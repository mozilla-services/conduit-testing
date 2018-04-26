import os
import time

from phabricator import Phabricator


def test_create_a_revision(bugzilla_secure_user_one):
    phab = Phabricator(
        host=os.getenv('PHABRICATOR_API_URL'),
        token=os.getenv('PHABRICATOR_API_KEY_1')
    )
    phab.update_interfaces()
    bug_data = {
        'product': 'Firefox',
        'component': 'Developer Tools',
        'summary': 'Test Bug',
        'version': 'unspecified'
    }
    bug_id = bugzilla_secure_user_one.bug_create(bug_data)

    # Grab the bug and let's see what data exists
    response = bugzilla_secure_user_one.bug_read(bug_id)
    bug_info = response['bugs'][0]
    assert 'summary' in bug_info
    assert 'product' in bug_info
    assert 'component' in bug_info
    assert 'version' in bug_info
    assert bug_info['summary'] == bug_data['summary']
    assert bug_info['product'] == bug_data['product']
    assert bug_info['component'] == bug_data['component']
    assert bug_info['version'] == bug_data['version']

    # Create a diff on Phabricator
    changes = [{
            "metadata": [],
            "oldPath": "arcanist.txt",
            "currentPath": "arcanist.txt",
            "awayPaths": [],
            "oldProperties": [],
            "newProperties": [],
            "type": 2,
            "fileType": 1,
            "commitHash": None,
            "hunks": [
                {
                    "oldOffset": "1",
                    "newOffset": "1",
                    "oldLength": "1",
                    "newLength": "2",
                    "addLines": 1,
                    "delLines": 0,
                    "isMissingOldNewline": False,
                    "isMissingNewNewline": False,
                    "corpus": " FIRST COMMENT\n+Second commit\n"
                }
            ]
        }]
    creatediff_response = phab.differential.creatediff(
        changes=changes,
        sourceMachine="grumpiermbp",
        sourcePath="\/Users\/chartjes\/phabricator-qa-dev\/",
        branch="default",
        sourceControlSystem="hg",
        sourceControlPath="\/",
        sourceControlBaseRevision="62a4917ca0075386afb8d694ad8910b0e76532fa",
        unitStatus="none",
        lintStatus="none",
        parentRevisionID="123456",
        authorPHID=phab.user.whoami().phid,
        repositoryUUID="12343545"
    )

    # Now create the revision using the diff information
    fields = {
            "title": "Commit message",
            "summary": "Summary",
            "testPlan": "QA create a revision",
            "reviewerPHIDs": [],
            "ccPHIDS": [],
            "bugzilla.bug-id": str(bug_id)
    }
    createrevision_response = phab.differential.createrevision(
        fields=fields,
        diffid=creatediff_response.diffid
    )
    assert createrevision_response.revisionid is not None
    assert createrevision_response.uri is not None

    '''
    Now read back details of the revision and make sure values are as 
    we expect them to be
    '''
    revision_id = createrevision_response.revisionid
    constraints = {"ids": [revision_id]}
    revisionsearch_response = phab.differential.revision.search(
        constraints=constraints
    )
    # We are expecting our records to be in the first element of the list
    data = revisionsearch_response.data[0]
    assert data['id'] == revision_id
    assert data['fields']['title'] == fields['title']

    '''
    Now we need to read the bug and look for our attachment that proves
    Phabricator has updated the bug
    
    The sleep statement is required because updating a bug does not happen
    instantly
    
    This test only ever generates one attachment for the bug
    '''
    time.sleep(8)
    response = bugzilla_secure_user_one.get_attachments(bug_id)
    bug_info = response['bugs']
    assert bug_info[str(bug_id)][0]['content_type'] == 'text/x-phabricator-request'
