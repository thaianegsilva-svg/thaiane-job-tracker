import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from collect import classify, convert, public_assisted, deduplicate, close_excluded

class EligibilityTests(unittest.TestCase):
    def test_close_excluded_preserves_contact_and_source_activity(self):
        job=dict(eligibility='excluded',applicationStatus='contacted',active=True,contactStatus='sent',rejectionReasons=['Figma obrigatório'])
        close_excluded([job])
        self.assertEqual(job['applicationStatus'],'closed')
        self.assertEqual(job['previousApplicationStatus'],'contacted')
        self.assertEqual(job['contactStatus'],'sent')
        self.assertTrue(job['active'])
        self.assertEqual(job['rejectionReasons'],['Figma obrigatório'])
    def test_pending_application_is_not_closed(self):
        job=dict(eligibility='pending',applicationStatus='preparing')
        close_excluded([job])
        self.assertEqual(job['applicationStatus'],'preparing')
    def test_duplicate_application_prefers_assisted_review(self):
        jobs=[dict(id='feed-1',source='Remotar',applyUrl='https://jobs.example/job/1/application?source=feed'),dict(id='review-1',source='LinkedIn',applyUrl='https://jobs.example/job/1/?source=linkedin')]
        result=deduplicate(jobs)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['id'],'review-1')
        self.assertEqual(result[0]['duplicateIds'],['feed-1'])
    def test_different_application_paths_remain_separate(self):
        self.assertEqual(len(deduplicate([dict(id='1',url='https://jobs.example/1'),dict(id='2',url='https://jobs.example/2')])),2)
    def job(self, **changes):
        j=dict(title='Designer Gráfico Sênior', description='Photoshop Illustrator identidade visual', workMode='remote',city=None,officeDays=None,portugueseConfirmed=True,requiresEnglish=False,salary=dict(min=8000,max=9000,currency='BRL',period='monthly'))
        j.update(changes)
        return classify(j)
    def test_eligible(self): self.assertEqual(self.job()['eligibility'],'eligible')
    def test_exactly_7000_is_excluded(self): self.assertEqual(self.job(salary=dict(min=7000,max=7000,currency='BRL',period='monthly'))['eligibility'],'excluded')
    def test_range_crosses_limit_pending(self): self.assertEqual(self.job(salary=dict(min=6000,max=9000,currency='BRL',period='monthly'))['eligibility'],'pending')
    def test_missing_salary_pending(self): self.assertEqual(self.job(salary={})['eligibility'],'pending')
    def test_annual_salary_not_monthly(self): self.assertEqual(self.job(salary=dict(min=96000,currency='BRL',period='annual'))['eligibility'],'pending')
    def test_pt_ad_does_not_confirm_language(self): self.assertEqual(self.job(portugueseConfirmed=False)['eligibility'],'pending')
    def test_english_excluded(self): self.assertEqual(self.job(requiresEnglish=True)['eligibility'],'excluded')
    def test_bh_two_days_eligible(self): self.assertEqual(self.job(workMode='hybrid',city='Belo Horizonte',officeDays=2)['eligibility'],'eligible')
    def test_bh_unknown_days_pending(self): self.assertEqual(self.job(workMode='hybrid',city='Belo Horizonte')['eligibility'],'pending')
    def test_hybrid_other_city_excluded(self): self.assertEqual(self.job(workMode='hybrid',city='São Paulo',officeDays=2)['eligibility'],'excluded')
    def test_three_days_excluded(self): self.assertEqual(self.job(workMode='hybrid',city='Belo Horizonte',officeDays=3)['eligibility'],'excluded')
    def test_ux_not_assumed(self): self.assertEqual(self.job(title='Senior Product Designer UX')['eligibility'],'excluded')
    def test_closed_not_eligible(self): self.assertEqual(self.job(active=False)['eligibility'],'excluded')
    def test_unmet_mandatory_skill_excluded(self): self.assertEqual(self.job(unmetRequirements=['Figma obrigatório não atendido'])['eligibility'],'excluded')
    def test_frontend_not_graphic_design(self): self.assertEqual(self.job(title='Especialista FrontEnd Design System')['eligibility'],'excluded')
    def test_private_message_fields_never_exported(self):
        safe = public_assisted(dict(id='linkedin-1',title='Designer',message='private body',conversationUrl='private link',sender='private sender',recipient='private recipient'))
        self.assertEqual(safe,dict(id='linkedin-1',title='Designer'))
    def test_private_thread_url_rejected(self):
        with self.assertRaises(ValueError): public_assisted(dict(url='https://www.linkedin.com/messaging/thread/private'))
    def test_source_salary_is_cents(self):
        job=convert(dict(id=1,title='Designer Gráfico',active=True,type='remote',jobSalary=dict(type='monthly',currency='BRL',**{'from':300000,'to':500000})), '2026-10-16T00:00:00+00:00')
        self.assertEqual(job['salary']['min'],3000)
        self.assertEqual(job['eligibility'],'excluded')
    def test_zero_is_undisclosed(self):
        job=convert(dict(id=1,title='Designer Gráfico',active=True,type='remote',jobSalary=dict(type='monthly',currency='BRL',**{'from':0,'to':0})), '2026-10-16T00:00:00+00:00')
        self.assertIsNone(job['salary']['min'])
        self.assertEqual(job['eligibility'],'pending')

if __name__=='__main__':unittest.main()
