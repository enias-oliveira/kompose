from rest_framework.test import APITestCase


class TestSongView(APITestCase):
    def setUp(self):
        self.song_1 = {
            "title": "Jumpsuit",
            "artist": {"name": "Twenty One Pilots"},
        }

        self.song_1_expected_response = {
            "id": 1,
            "title": "Jumpsuit",
            "artist": {"id": 1, "name": "Twenty One Pilots"},
            "votes": 1,
        }

        self.song_2 = {
            "title": "Levitate",
            "artist": {"name": "Twenty One Pilots"},
        }

        self.song_2_expected_response = {
            "id": 2,
            "title": "Levitate",
            "artist": {"id": 1, "name": "Twenty One Pilots"},
            "votes": 1,
        }

        self.base_url = "/api/songs/"

    def test_create_song(self):
        song_1_post_response = self.client.post(
            self.base_url, self.song_1, format="json"
        )

        self.assertDictEqual(
            self.song_1_expected_response,
            song_1_post_response.json(),
        )

    def test_invalid_create_song(self):
        invalid_post_response = self.client.post(self.base_url, {}, format="json")
        self.assertEqual(invalid_post_response.status_code, 400)

    def test_retrieve_song(self):
        song_post_response = self.client.post(self.base_url, self.song_2, format="json")
        song_post_id = song_post_response.json()["id"]

        song_get_response = self.client.get(f"{self.base_url}{song_post_id}/").json()

        self.song_2_expected_response["id"] = song_post_id

        self.assertDictEqual(self.song_2_expected_response, song_get_response)

    def test_list_all_songs(self):
        self.client.post(self.base_url, self.song_1, format="json")
        self.client.post(self.base_url, self.song_2, format="json")

        songs = self.client.get(self.base_url)

        self.assertEqual(len(songs.json()), 2)

    def test_updata_song(self):
        song_post_response = self.client.post(self.base_url, self.song_1, format="json")
        song_post_id = song_post_response.json()["id"]

        song_update_response = self.client.put(
            f"{self.base_url}{song_post_id}/",
            {"title": "Salad Days", "artist": {"name": "Twenty One Pilots"}},
            format="json",
        )

        song_get_response = self.client.get(f"{self.base_url}{song_post_id}/").json()

        self.song_2_expected_response["id"] = song_post_id

        self.assertDictEqual(
            {
                "id": song_post_id,
                "title": "Salad Days",
                "artist": {"id": song_post_id, "name": "Twenty One Pilots"},
                "votes": 1,
            },
            song_get_response,
        )
