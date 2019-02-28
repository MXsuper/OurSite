from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    def create(self, validated_data):
        """
        创建用户
        """
        user = super().create(validated_data)
        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user

    class Meta:
        model = User
        fields = ('username', 'password','token')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'gender', 'location', 'phone', 'birthday', 'introduction')


class DoctorDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'gender', 'location', 'phone', 'birthday', 'introduction',
                  'identity_name', 'identity_number', 'doctor_number', 'doctor_hospital')


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    class Meta:
        model = User
        fields = ('nickname', 'gender', 'location', 'phone', 'birthday', 'introduction',
                  'is_doctor', 'identity_name', 'identity_number', 'doctor_number', 'doctor_hospital')


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    更新用户密码
    """
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('password',)
