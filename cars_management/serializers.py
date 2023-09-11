from rest_framework import serializers
from .models import *

from .models import Car, Maintenance, Reclamation, SteeringAxleType, DriveAxleType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class TechnicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technics
        fields = '__all__'


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineModels
        fields = '__all__'


class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransmissionModels
        fields = '__all__'


class DrivingBridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteeringAxleType
        fields = '__all__'


class ControlledBridgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriveAxleType
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamation
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    technic = TechnicSerializer()
    engine = EngineSerializer()
    transmission = TransmissionSerializer()
    driving_bridge = DrivingBridgeSerializer()
    controlled_bridge = ControlledBridgeSerializer()
    service_company = ServiceSerializer()
    client = UserSerializer()
    class Meta:
        model = Car
        fields = '__all__'


class ServiceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCompany
        fields = '__all__'


class TypeMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceType
        fields = '__all__'


class FailureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailureNodes
        fields = '__all__'

class RecoveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestorationMethods
        fields = '__all__'


class MaintenanceSerializer(serializers.ModelSerializer):
    type = TypeMaintenanceSerializer()
    service_company = ServiceCompanySerializer()
    class Meta:
        model = Maintenance
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    node_failure = FailureSerializer()
    method_recovery = RecoveryMethodSerializer()
    service_company = ServiceCompanySerializer()
    class Meta:
        model = Reclamation
        fields = '__all__'