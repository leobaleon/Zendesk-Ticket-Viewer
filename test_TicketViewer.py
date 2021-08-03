import unittest
import TicketViewer

class TestTicketViewer(unittest.TestCase):
    def setUp(self):
        self.ticket_viewer = TicketViewer.TicketViewer()

    def tearDown(self):
        pass

    # get_json() tests
    def test_get_json_valid_url(self):
        url = f'{self.ticket_viewer.original_url}.json?page[size]=25'
        self.assertNotEqual('-1', self.ticket_viewer.get_json(url))

    def test_get_json_invalid_url(self):
        url = 'bad url'
        self.assertEqual('-1', self.ticket_viewer.get_json(url))

    # solution() tests
    def test_solution_normal_behavior(self):
        self.assertEqual(0, self.ticket_viewer.solution())

    def test_solution_could_not_connect(self):
        self.ticket_viewer.json_data = self.ticket_viewer.get_json('')
        self.assertEqual(-1, self.ticket_viewer.solution())

if __name__ == '__main__':
    unittest.main()