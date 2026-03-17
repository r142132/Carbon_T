import unittest

from Stage_Survey import Survey


class SurveyValidationTests(unittest.TestCase):
    def test_other_requires_detail(self):
        errors = Survey.error_message(None, {
            'env_job_type': '其他',
            'env_job_type_other': '',
        })
        self.assertEqual(
            errors,
            {'env_job_type_other': '您勾選了「其他」，請填寫具體工作類別。'}
        )

    def test_non_other_forbids_detail(self):
        errors = Survey.error_message(None, {
            'env_job_type': '企業內部永續、ESG、環安衛或環境管理人員',
            'env_job_type_other': '自填內容',
        })
        self.assertEqual(
            errors,
            {'env_job_type_other': '只有在勾選「其他」時才能填寫說明。'}
        )

    def test_other_with_detail_passes(self):
        errors = Survey.error_message(None, {
            'env_job_type': '其他',
            'env_job_type_other': '地方政府淨零專案管理',
        })
        self.assertIsNone(errors)


if __name__ == '__main__':
    unittest.main()
