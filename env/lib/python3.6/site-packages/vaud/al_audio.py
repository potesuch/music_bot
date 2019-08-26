from time import sleep
from .al_audio_base import AlAudioBase


class AlAudio(AlAudioBase):

    def __init__(self, uid, cookies):
        super(AlAudio, self).__init__()
        """
        :param uid: user_id
        :type uid: int
        :param cookies:
        :type cookies: dict
        """
        self._uid = int(uid)
        self._cookies = cookies

    def main(self, as_tuples_list=False):
        """
        :param as_tuples_list:
         Get response as [tuple,tuple,..], if as_tuples_list = True
         Default as [dict, dict, ..]
        :type bool
        :return:
        """
        self._response_as_tuples_list = bool(as_tuples_list)
        self._fill_playlist()
        self._parse_playlist()

        response = list(self._list_decoded_tracks)
        if 0 < self.limit < len(response):
            response = response[0:self.limit]
        return response

    def set_playlist_id(self, idx):
        """
        :param idx:
        :type int
        :return:
        """
        self._playlist_id = idx

    def _fill_playlist(self, offset=0):
        response = self._get_playlist_response(offset)

        check_type = response.get('type', '') != 'playlist'

        if check_type or len(self._playlist) >= self.limit > 0:
            return

        self._playlist += response.get('list', [])

        if self.force_data or int(response.get('hasMore', 0)) != 0:
            sleep(self._sleep_time)  # spam-ban. sleeping.
            self._fill_playlist(response.get('nextOffset'))

    def _parse_playlist(self):
        for i in self._playlist:
            self._parse_playlist_func(i)
        self._parse_list_items(self._list_post_load)
        self._list_post_load = []
