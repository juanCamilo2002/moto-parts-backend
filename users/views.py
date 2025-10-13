from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import RegisterSerializer, UserSerializer, LogoutSerializer, LoginSerializer
from .models import User

@extend_schema(
    tags=['Auth'],
    summary='Registrar un nuevo usuario',
    description="Crea una cuenta nueva en el sistema. Por defecto, todos los usuarios registrados son **vendedores (seller)**.",
    request=RegisterSerializer,
    responses={
         201: OpenApiResponse(response=UserSerializer, description="Usuario registrado correctamente."),
        400: OpenApiResponse(description="Datos inválidos o usuario ya existente."),
    }
)
class ResgisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = RegisterSerializer



@extend_schema(
    tags=["Auth"],
    summary="Obtener perfil del usuario autenticado",
    description="Devuelve la información del usuario autenticado (email, nombre, rol, etc.).",
    responses={
        200: OpenApiResponse(response=UserSerializer, description="Perfil del usuario autenticado."),
        401: OpenApiResponse(description="No autenticado."),
    },
)
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        return self.request.user
    
    
    
@extend_schema(
    tags=["Auth"],
    summary="Cerrar sesión",
    description="Invalida el token de actualización (refresh token) para finalizar la sesión.",
    request=LogoutSerializer,
    responses={
        205: OpenApiResponse(description="Sesión cerrada correctamente."),
        400: OpenApiResponse(description="Token inválido o ya invalidado."),
    },
)
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
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
    
@extend_schema(
    tags=["Auth"],
    summary="Iniciar sesión",
    description=(
        "Autentica al usuario con **email** y **password**, devolviendo los tokens "
        "`access` y `refresh` para futuras peticiones autenticadas."
    ),
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "example": "admin@example.com"},
                "password": {"type": "string", "example": "12345"}
            },
            "required": ["email", "password"]
        }
    },
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "Token de acceso JWT"},
                    "refresh": {"type": "string", "description": "Token de actualización JWT"}
                }
            },
            description="Inicio de sesión exitoso. Devuelve los tokens de autenticación."
        ),
        401: OpenApiResponse(description="Credenciales inválidas.")
    }
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Documentación extendida para iniciar sesión con JWT."""
    pass


# Documentación personalizada del refresh token
@extend_schema(
    tags=["Auth"],
    summary="Refrescar token de acceso",
    description="Renueva el token de acceso usando un `refresh token` válido.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "refresh": {"type": "string", "example": "eyJhbGciOiJIUzI1NiIs..."}
            },
            "required": ["refresh"]
        }
    },
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "Nuevo token de acceso JWT"}
                }
            },
            description="Token de acceso renovado correctamente."
        ),
        401: OpenApiResponse(description="El refresh token no es válido o ha expirado.")
    }
)
class CustomTokenRefreshView(TokenRefreshView):
    """Documentación extendida para refrescar el token de acceso."""
    pass