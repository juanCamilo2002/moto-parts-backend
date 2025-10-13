from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .serializers import RegisterSerializer, UserSerializer
from .models import User

class ResgisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user
    
class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "El token de actualización (refresh) es obligatorio."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "El token de actualización no es válido o ya fue invalidado."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {"detail": "No se pudo cerrar la sesión correctamente."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"detail": "Sesión cerrada correctamente."}, 
            status=status.HTTP_205_RESET_CONTENT
        )