import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_eridan.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from requests.views import ClientRequestListView
from requests.models import ClientRequest

User = get_user_model()

def test_executor_filtering():
    # Create test users
    executor_user = User.objects.create_user(username='executor', password='testpass', role='executor')
    admin_user = User.objects.create_user(username='admin', password='testpass', role='admin')

    # Create test requests
    request1 = ClientRequest.objects.create(
        client_name='Client1',
        phone='123456789',
        client_email='client1@example.com',
        description='Test request 1',
        status='in_progress',
        assigned_to=executor_user
    )
    request2 = ClientRequest.objects.create(
        client_name='Client2',
        phone='987654321',
        client_email='client2@example.com',
        description='Test request 2',
        status='completed',
        assigned_to=executor_user
    )
    request3 = ClientRequest.objects.create(
        client_name='Client3',
        phone='555555555',
        client_email='client3@example.com',
        description='Test request 3',
        status='new',
        assigned_to=executor_user
    )
    request4 = ClientRequest.objects.create(
        client_name='Client4',
        phone='111111111',
        client_email='client4@example.com',
        description='Test request 4',
        status='in_progress',
        assigned_to=admin_user  # Assigned to different user
    )

    factory = RequestFactory()

    # Test executor with status='all'
    request = factory.get('/client_requests/?status=all')
    request.user = executor_user
    view = ClientRequestListView()
    view.request = request
    queryset = view.get_queryset()
    results = list(queryset)
    print(f"Executor 'all' status: {len(results)} requests")
    expected_ids = {request1.id, request2.id}
    actual_ids = {r.id for r in results}
    if actual_ids == expected_ids:
        print("PASS: Executor sees only in_progress and completed assigned requests")
    else:
        print(f"FAIL: Expected {expected_ids}, got {actual_ids}")

    # Test executor with status='in_progress'
    request = factory.get('/client_requests/?status=in_progress')
    request.user = executor_user
    view = ClientRequestListView()
    view.request = request
    queryset = view.get_queryset()
    results = list(queryset)
    print(f"Executor 'in_progress' status: {len(results)} requests")
    expected_ids = {request1.id}
    actual_ids = {r.id for r in results}
    if actual_ids == expected_ids:
        print("PASS: Executor sees only assigned in_progress requests")
    else:
        print(f"FAIL: Expected {expected_ids}, got {actual_ids}")

    # Test admin with status='all' (should see all)
    request = factory.get('/client_requests/?status=all')
    request.user = admin_user
    view = ClientRequestListView()
    view.request = request
    queryset = view.get_queryset()
    results = list(queryset)
    print(f"Admin 'all' status: {len(results)} requests")
    if len(results) == 4:
        print("PASS: Admin sees all requests")
    else:
        print(f"FAIL: Expected 4, got {len(results)}")

    # Clean up
    ClientRequest.objects.filter(id__in=[request1.id, request2.id, request3.id, request4.id]).delete()
    User.objects.filter(username__in=['executor', 'admin']).delete()

if __name__ == '__main__':
    test_executor_filtering()
