from lxml import etree

from app.auth.models import Users
from app.releases.models import Release
from app.testplans.models import TestPlan
from app.testcases.models import TestCase

import os

def xml_creation(db_session, release_id, root_path):
    try:
        cur_release = Release.query.filter(Release.id == release_id).first()
        test_plan_counter = 0

        release_tag = etree.Element('release')
        release_properties = etree.SubElement(release_tag, 'release_properties')
        release_title = etree.SubElement(release_properties, 'name')
        release_title.text = cur_release.name
        release_description = etree.SubElement(release_properties, 'description')
        release_description.text = cur_release.description
        release_status = etree.SubElement(release_properties, 'status')
        release_status.text = cur_release.status
        release_status = etree.SubElement(release_properties, 'start_date')
        release_status.text = cur_release.open_date
        release_status = etree.SubElement(release_properties, 'close_date')
        release_status.text = cur_release.close_date

        test_plans = TestPlan.query.all()
        test_plans_parse = etree.SubElement(release_tag, 'test_plans')
        for item in test_plans:
            test_plan_properties = etree.SubElement(release_tag, 'test_plan_{}'.format(test_plan_counter))
            testplan_title = etree.SubElement(test_plan_properties, 'name')
            testplan_title.text = item.name
            testplan_description = etree.SubElement(test_plan_properties, 'description')
            testplan_description.text = item.description
            testplan_status = etree.SubElement(test_plan_properties, 'status')
            testplan_status.text = item.status
            testplan_cases = etree.SubElement(test_plan_properties, 'cases')

            test_cases = TestCase.query.filter(TestCase.testplan_id == item.id).all()
            test_case_counter = 0
            for case in test_cases:
                test_case_properties = etree.SubElement(testplan_cases, 'test_case_{}'.format(test_case_counter))
                testcase_title = etree.SubElement(test_case_properties, 'name')
                testcase_title.text = case.name
                testcase_description = etree.SubElement(test_case_properties, 'description')
                testcase_description.text = case.description
                testcase_status = etree.SubElement(test_case_properties, 'status')
                testcase_status.text = case.status

                test_case_counter += 1

            test_plan_counter += 1

        path_to_xml = "{}/{}-{}.xml".format(root_path, cur_release.name, cur_release.id)

        doc = etree.ElementTree(release_tag)

        doc.write(path_to_xml, pretty_print=True)

    # doc = open(path_to_xml, 'w')
    # print(etree.tostring(release_tag, pretty_print=True), file=doc)
    # doc.close()

        cur_release.xml = cur_release.id
    except Exception as err:
        print('An error occered:\n', err)

    return True
