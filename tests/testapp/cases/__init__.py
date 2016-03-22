from django.test import TestCase
from django.conf import settings
from rescuests.models import Request
from model_mommy import mommy

import mock

outer_func = mock.Mock()


class BaseTestCase(TestCase):

  def test_defaults(self):
    request = mommy.make(Request)

    self.assertEqual(Request.NEW, request.status)
    self.assertEqual(3, request.max_retries)
    self.assertEqual(0, request.retries)
    self.assertEqual("", request.comment)
    self.assertIsNone(request.last_try)

  def test_mocked_call_with_function_import_string(self):

    with Request.mock("tests.testapp.cases.outer_func"):
      request = mommy.make(Request, url = "testurl")
      request.run()

    outer_func.assert_called_with(200, request.url)
    self.assertEqual(Request.READY, request.status)

  def test_mocked_call_with_direct_function(self):
    inner_func = mock.Mock()

    with Request.mock(inner_func):
      request = mommy.make(Request, url = "testurl")
      request.run()

    inner_func.assert_called_with(200, request.url)
    self.assertEqual(Request.READY, request.status)

  def test_mocked_call_with_other_status(self):
    inner_func = mock.Mock()

    with Request.mock(inner_func, 404):
      request = mommy.make(Request, url = "testurl")
      request.run()

    inner_func.assert_called_with(404, request.url)
    self.assertEqual(Request.RETRYING, request.status)

  def test_failed_status(self):
    inner_func = mock.Mock()

    with Request.mock(inner_func, 404):
      request = mommy.make(Request, url = "testurl")
      for i in range(request.max_retries):
        request.run()
        self.assertEqual(Request.RETRYING, request.status)

      request.run()
      self.assertEqual(Request.FAILED, request.status)

