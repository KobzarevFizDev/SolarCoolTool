from unittest import TestCase, main

from Models.solar_editor_model import SolarEditorModel
from images_indexer import ImagesIndexer


class SolarEditorModelTest(TestCase):
    def setUp(self) -> None:
        self.model = SolarEditorModel(ImagesIndexer("C:\\SolarImages"))

    def test_need_cache_images_of_channel_case1(self):
        message = "test_need_cache_images_of_channel_case1 is wrong"
        self.model.currentChannelModel.setCurrentChannel(193)
        self.assertTrue(self.model.currentChannelModel.newChannelWasSelected, message)

    def test_need_cache_images_of_channel_case2(self):
        message = "test_need_cache_images_of_channel_case2 is wrong"
        self.model.currentChannelModel.setCurrentChannel(193)
        self.model.currentChannelModel.setCurrentChannel(193)
        self.assertFalse(self.model.currentChannelModel.newChannelWasSelected, message)

    def tearDown(self) -> None:
        pass

if __name__ == "__main__":
    main()