from unittest import TestCase
from django.urls import reverse
from utils.pagination import make_pagination_range
from recipes.tests.test_recipe_base import RecipeTestBase


class PaginationTest(RecipeTestBase, TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa E501
        # Current page = 1 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty Page = 2 - Middle Page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD PAGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        # Current page = 4 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD PAGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD PAGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)

        # Current page = 12 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD PAGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        # Current page = 21 - Qty Page = 2 - Middle Page = 2
        # HERE RANGE SHOULD PAGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_pagination_check_recipes_and_pages(self):
        # response
        recipes_test = []

        for i in range(8):
            recipes_test.append(
                self.make_recipe(
                    slug=f'slug-{i}',
                    title=f"Receita da mamãe {i}",
                    author_data={'username': f'usuario{i}'}
                )
            )

        response = reverse('recipes:home')

        response1 = self.client.get(f'{response}?page=1')
        response_context_recipes_page1 = response1.context['recipes']

        response2 = self.client.get(f'{response}?page=2')
        response_context_recipes_page2 = response2.context['recipes']

        self.assertEqual(len(response_context_recipes_page1), 6)
        self.assertEqual(len(response_context_recipes_page2), 2)

        self.assertIn(recipes_test[0], response_context_recipes_page2)
        self.assertIn(recipes_test[1], response_context_recipes_page2)
        self.assertIn(recipes_test[2], response_context_recipes_page1)
        self.assertIn(recipes_test[3], response_context_recipes_page1)
        self.assertIn(recipes_test[4], response_context_recipes_page1)
        self.assertIn(recipes_test[5], response_context_recipes_page1)
        self.assertIn(recipes_test[6], response_context_recipes_page1)
        self.assertIn(recipes_test[7], response_context_recipes_page1)

    def test_pagination_check_execpt_current_page(self):
        response = reverse('recipes:home')
        response_page = self.client.get(f'{response}?page=teste')

        self.assertEqual(
            1,
            response_page.context['pagination_range']['current_page']
        )
