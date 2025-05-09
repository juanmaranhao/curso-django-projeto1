import pytest
from tests.functional_tests.authors.base import AuthorsBaseTest
from django.contrib.auth import get_user_model
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.browser import make_chrome_browser

User = get_user_model()


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password
        )

        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(
            By.CLASS_NAME, 'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulário
        form.submit()

        # Usuário vê a messagem de login com sucesso e seu nome
        # Re-locate the body element after form submission to avoid
        # stale element reference
        wait = WebDriverWait(self.browser, timeout=2)
        wait.until(lambda _: self.browser.find_element(
            By.TAG_NAME, 'body').is_displayed())

        body_element = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(
            f'You are logged in with {user.username}.',
            body_element.text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(
            By.CLASS_NAME, 'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário envia valores vazios
        username_field.send_keys(' ')
        password_field.send_keys(' ')

        # Usuário envia o formulário
        form.submit()

        wait = WebDriverWait(make_chrome_browser(), timeout=2)
        wait.until(lambda _: self.browser.find_element(
            By.TAG_NAME, 'body').is_displayed())

        body_element = self.browser.find_element(By.TAG_NAME, 'body')
        # Usuário vê a messagem de erro ao tentar logar
        self.assertIn(
            'Invalid username or password',
            body_element.text
        )

    def test_login_with_invalid_credentials(self):
        # Usuário abre a página de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(
            By.CLASS_NAME, 'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita seu usuário e senha inválidos
        username_field.send_keys('InvalidUser')
        password_field.send_keys('InvalidPassword')

        # Usuário envia o formulário
        form.submit()
        # Re-locate the body element after form submission to avoid
        # stale element reference
        # self.browser.refresh()
        wait = WebDriverWait(make_chrome_browser(), timeout=2)
        wait.until(lambda _: self.browser.find_element(
            By.TAG_NAME, 'body').is_displayed())

        body_element = self.browser.find_element(By.TAG_NAME, 'body')

        self.assertIn(
            'Invalid credentials',
            body_element.text
        )
