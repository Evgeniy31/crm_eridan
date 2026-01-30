import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_eridan.settings')
django.setup()

from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from requests.views import assign_executor
from requests.models import ClientRequest
from notifications.models import Notification
from repairs.models import RepairRequest
from clients.models import Client

User = get_user_model()

def test_notification_creation():
    # Create test users
    try:
        executor_user = User.objects.create_user(username='test_executor', password='testpass', role='executor')
        admin_user = User.objects.create_user(username='test_admin', password='testpass', role='admin')
    except:
        executor_user = User.objects.get(username='test_executor')
        admin_user = User.objects.get(username='test_admin')

    # Create test client
    try:
        client = Client.objects.create(
            name='Test Client',
            phone='123456789',
            email='test@example.com'
        )
    except:
        client = Client.objects.get(name='Test Client')

    # Create test request
    try:
        request_obj = ClientRequest.objects.create(
            client=client,
            description='Test request for notification',
            status='new'
        )
    except:
        request_obj = ClientRequest.objects.filter(description='Test request for notification').first()
        if not request_obj:
            request_obj = ClientRequest.objects.create(
                client=client,
                description='Test request for notification',
                status='new'
            )

    # Create test repair request
    try:
        repair_request = RepairRequest.objects.create(
            organization_name='Test Org',
            client_last_name='Test',
            client_first_name='Client',
            phone='123456789',
            email='test@example.com',
            equipment_name='Test Equipment',
            issue_description='Test issue',
            status='new'
        )
    except:
        repair_request = RepairRequest.objects.filter(organization_name='Test Org').first()
        if not repair_request:
            repair_request = RepairRequest.objects.create(
                organization_name='Test Org',
                client_last_name='Test',
                client_first_name='Client',
                phone='123456789',
                email='test@example.com',
                equipment_name='Test Equipment',
                issue_description='Test issue',
                status='new'
            )

    factory = RequestFactory()

    # Test assigning executor to client request
    print("Testing notification for ClientRequest assignment...")
    request = factory.post(f'/assign_executor/client/{request_obj.id}/', {'executor': executor_user.id})
    request.user = admin_user
    response = assign_executor(request, 'client', request_obj.id)

    # Check if notification was created
    notifications = Notification.objects.filter(user=executor_user, title='Вам назначена заявка')
    if notifications.exists():
        notification = notifications.last()
        expected_message = f'Вам назначена заявка {request_obj.request_number} для выполнения.'
        if notification.message == expected_message:
            print("PASS: Notification created for ClientRequest assignment")
        else:
            print(f"FAIL: Expected message '{expected_message}', got '{notification.message}'")
    else:
        print("FAIL: No notification created for ClientRequest assignment")

    # Test assigning executor to repair request
    print("Testing notification for RepairRequest assignment...")
    request = factory.post(f'/assign_executor/repair/{repair_request.id}/', {'executor': executor_user.id})
    request.user = admin_user
    response = assign_executor(request, 'repair', repair_request.id)

    # Check if notification was created
    notifications = Notification.objects.filter(user=executor_user, title='Вам назначена заявка')
    if notifications.exists():
        notification = notifications.last()
        expected_message = f'Вам назначена заявка на ремонт #{repair_request.id} для выполнения.'
        if notification.message == expected_message:
            print("PASS: Notification created for RepairRequest assignment")
        else:
            print(f"FAIL: Expected message '{expected_message}', got '{notification.message}'")
    else:
        print("FAIL: No notification created for RepairRequest assignment")

    # Clean up
    Notification.objects.filter(user=executor_user).delete()
    ClientRequest.objects.filter(id=request_obj.id).delete()
    RepairRequest.objects.filter(id=repair_request.id).delete()
    Client.objects.filter(id=client.id).delete()
    User.objects.filter(username__in=['test_executor', 'test_admin']).delete()

    print("Test completed.")

if __name__ == '__main__':
    test_notification_creation()
