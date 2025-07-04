from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.views import LavagemViewSet, FuncionarioViewSet  # Importações das views
from app.auth.views import UserInfoView

# Criação do roteador
router = DefaultRouter()
router.register(r'agendamentos', LavagemViewSet, basename='agendamentos')  # Rota para Lavagem
router.register(r'funcionarios', FuncionarioViewSet, basename='funcionarios')  # Rota para Funcionario

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs do DRF
    path('api-auth/', include('rest_framework.urls')),  # Permite o login do DRF
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Geração de tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Renovação de tokens
    path('api/user-info/', UserInfoView.as_view(), name='user_info'),  # Informações do usuário

    # URL para edição do agendamento de lavagem (usando ID na URL)
    # path('lavagens/<int:id>/', LavagemEditView.as_view(), name='lavagem-edit'),

    # Registro das rotas com o roteador
    path('api/', include(router.urls)),  # Inclui as rotas registradas no router (agendamentos e funcionarios)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Configuração para servir arquivos de mídia
