from django.test import TestCase
from projects.models import PersonalInfo, Education, Job, Skillset, Skill, LangSkill, ProjectCategory, Project, Price, Post, Comment


class PersonalInfoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        PersonalInfo.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        personal_info = PersonalInfo.objects.get(id=1)
        field_label = personal_info._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        personal_info = PersonalInfo.objects.get(id=1)
        field_label = personal_info._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_first_name_max_length(self):
        personal_info = PersonalInfo.objects.get(id=1)
        max_length = personal_info._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 250)

    def test_last_name_max_length(self):
        personal_info = PersonalInfo.objects.get(id=1)
        max_length = personal_info._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 250)

    def test_object_name_is_last_name_comma_first_name(self):
        personal_info = PersonalInfo.objects.get(id=1)
        expected_object_name = '{0}, {1}'.format(personal_info.first_name, personal_info.last_name)

        self.assertEquals(expected_object_name, str(personal_info))


class EducationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Education.objects.create(
            school_name='Tbilisi State University',
            institute_or_faculty='Institute of Economics',
            department='Department of Economics',
            qualification='Economist',
            location='Kyiv, Ukraine',
            start_date='2014-09-01',
            completion_date='2017-09-15',
        )

    def test_school_name_label(self):
        school_name = Education.objects.get(id=1)
        field_label = school_name._meta.get_field('school_name').verbose_name
        self.assertEquals(field_label, 'school name')

    def test_school_name_max_length(self):
        school_name = Education.objects.get(id=1)
        max_length = school_name._meta.get_field('school_name').max_length
        self.assertEquals(max_length, 250)

    def test_institute_or_faculty_name_label(self):
        institute_or_faculty = Education.objects.get(id=1)
        field_label = institute_or_faculty._meta.get_field('institute_or_faculty').verbose_name
        self.assertEquals(field_label, 'institute or faculty')

    def test_institute_or_faculty_max_length(self):
        institute_or_faculty = Education.objects.get(id=1)
        max_length = institute_or_faculty._meta.get_field('institute_or_faculty').max_length
        self.assertEquals(max_length, 250)

    def test_department_name_label(self):
        department = Education.objects.get(id=1)
        field_label = department._meta.get_field('department').verbose_name
        self.assertEquals(field_label, 'department')

    def test_department_name_max_length(self):
        department = Education.objects.get(id=1)
        max_length = department._meta.get_field('department').max_length
        self.assertEquals(max_length, 250)

    def test_location_name_label(self):
        location = Education.objects.get(id=1)
        field_label = location._meta.get_field('location').verbose_name
        self.assertEquals(field_label, 'location')

    def test_location_name_max_length(self):
        location = Education.objects.get(id=1)
        max_length = location._meta.get_field('department').max_length
        self.assertEquals(max_length, 250)


class JobModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Job.objects.create(
            company='Research Center of Huawei Technologies Co. Ltd.',
            title='Thermal research engineer',
            description='Thermal management and IC package design research, cooling solution development for telecom, computing and consumer products',
            start_date='2017-09-15',
            completion_date='2019-09-15',
        )

    def test_company_name_label(self):
        company = Job.objects.get(id=1)
        field_label = company._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'company')

    def test_company_name_max_length(self):
        company = Job.objects.get(id=1)
        max_length = company._meta.get_field('company').max_length
        self.assertEquals(max_length, 250)

    def test_title_label(self):
        title = Job.objects.get(id=1)
        field_label = title._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        title = Job.objects.get(id=1)
        max_length = title._meta.get_field('title').max_length
        self.assertEquals(max_length, 250)

    def test_description_label(self):
        description = Job.objects.get(id=1)
        field_label = description._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')


class SkillsetModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Skillset.objects.create(
            name='Computer-Aided-Engineering',
        )

    def test_skillset_name_label(self):
        name = Skillset.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_skillset_name_max_length(self):
        name = Skillset.objects.get(id=1)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)


class SkillModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Skill.objects.create(
            name='Computer-Aided-Engineering',
        )

    def test_skill_name_label(self):
        name = Skill.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_skill_name_max_length(self):
        name = Skill.objects.get(id=1)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)


class LangSkillModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        LangSkill.objects.create(
            name='English',
        )

    def test_langskill_name_label(self):
        name = LangSkill.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_langskill_name_max_length(self):
        name = LangSkill.objects.get(id=1)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)


class ProjectCategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        ProjectCategory.objects.create(
            name='Engineering',
        )

    def test_projectcategory_name_label(self):
        name = ProjectCategory.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_projectcategory_name_max_length(self):
        name = ProjectCategory.objects.get(id=1)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)


class PriceModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Set up non-modified objects used by all test methods."""
        Price.objects.create(
            type='Simple',
            support='Mail Support',
            name='Thermal analysis',
            instrument='Fluent',
            description='Forced convection',
            time_delivery='5',
            price='250',

        )

    def test_type_name_label(self):
        type = Price.objects.get(id=1)
        field_label = type._meta.get_field('type').verbose_name
        self.assertEquals(field_label, 'type')

    def test_type_name_max_length(self):
        type = Price.objects.get(id=1)
        max_length = type._meta.get_field('type').max_length
        self.assertEquals(max_length, 10)

    def test_support_name_label(self):
        support = Price.objects.get(id=1)
        field_label = support._meta.get_field('support').verbose_name
        self.assertEquals(field_label, 'support')

    def test_support_name_max_length(self):
        support = Price.objects.get(id=1)
        max_length = support._meta.get_field('support').max_length
        self.assertEquals(max_length, 250)

    def test_price_name_label(self):
        name = Price.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_price_name_max_length(self):
        name = Price.objects.get(id=1)
        max_length = name._meta.get_field('name').max_length
        self.assertEquals(max_length, 250)
