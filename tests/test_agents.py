"""Static custom-agent contract checks; these do not prove client discovery."""

from pathlib import Path
import re
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / '.codex' / 'agents'
NAMES = {
    'architect', 'product-analyst', 'designer', 'implementer', 'reviewer',
    'qa-specialist', 'security-specialist', 'release-specialist',
}
RESULT_FIELDS = (
    'TASK ID', 'OBJECTIVE', 'SCOPE', 'INPUTS', 'ASSUMPTIONS', 'DEPENDENCIES',
    'FILES INVOLVED', 'ACTION TAKEN', 'EVIDENCE', 'TESTS', 'RISKS',
    'OPEN ISSUES', 'STATUS',
)
STATUSES = (
    'NOT_STARTED', 'IN_PROGRESS', 'BLOCKED', 'NEEDS_REVIEW', 'VERIFIED', 'FAILED',
)


class CustomAgentTests(unittest.TestCase):
    def profiles(self):
        return {p.stem: tomllib.loads(p.read_text()) for p in AGENTS.glob('*.toml')}

    def test_eight_requested_profiles_exist(self):
        self.assertEqual(set(self.profiles()), NAMES)

    def test_profiles_use_documented_fields_without_permission_overrides(self):
        profiles = self.profiles()
        self.assertTrue(profiles, 'No custom agent profiles were found')
        for name, profile in profiles.items():
            with self.subTest(agent=name):
                self.assertEqual(set(profile), {'name', 'description', 'developer_instructions'})
                self.assertEqual(profile['name'], name)
                self.assertTrue(profile['description'].strip())
                self.assertTrue(profile['developer_instructions'].strip())

    def test_result_contract_and_lifecycle_are_available_in_each_profile(self):
        profiles = self.profiles()
        self.assertTrue(profiles, 'No custom agent profiles were found')
        for name, profile in profiles.items():
            instructions = profile['developer_instructions']
            with self.subTest(agent=name):
                for field in RESULT_FIELDS:
                    self.assertIn(field, instructions)
                for status in STATUSES:
                    self.assertIn(status, instructions)
                self.assertIn('independent', instructions.lower())
                self.assertIn('self-review', instructions.lower())

    def test_recommended_skills_are_real_and_selective(self):
        profiles = self.profiles()
        self.assertTrue(profiles, 'No custom agent profiles were found')
        for name, profile in profiles.items():
            with self.subTest(agent=name):
                match = re.search(r'^Recommended skills: (.+)$',
                                  profile['developer_instructions'], re.MULTILINE)
                self.assertIsNotNone(match)
                skills = [s.strip() for s in match.group(1).split(',')]
                self.assertGreater(len(skills), 0)
                self.assertLessEqual(len(skills), 7)
                for skill in skills:
                    self.assertTrue((ROOT / 'skills' / skill / 'SKILL.md').is_file(), skill)


if __name__ == '__main__':
    unittest.main()
