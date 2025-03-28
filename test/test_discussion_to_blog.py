import unittest
import os
import discussions_to_blog


class TestDiscussionsToBlogRun(unittest.TestCase):

    def test_run_created_event(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        discussions_to_blog.run(
            output_dir=os.path.join(base_dir, "resources/posts"),
            event_file_path="resources/create_event.json",
            workspace_root="resources/workspace",
        )

    def test_run_body_edited_event(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        discussions_to_blog.run(
            output_dir=os.path.join(base_dir, "resources/posts"),
            event_file_path="resources/edit_body_event.json",
            workspace_root="resources/workspace",
        )

    def test_run_title_edited_event(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        discussions_to_blog.run(
            output_dir=os.path.join(base_dir, "resources/posts"),
            event_file_path="resources/edit_title_event.json",
            workspace_root="resources/workspace",
        )

    def test_run_delete_event(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        discussions_to_blog.run(
            output_dir=os.path.join(base_dir, "resources/posts"),
            event_file_path="resources/delete_event.json",
            workspace_root="resources/workspace",
        )


if __name__ == '__main__':
    unittest.main()
