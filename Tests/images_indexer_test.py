from unittest import TestCase, main
from images_indexer import ImagesIndexer

class ImagesIndexerTest(TestCase):
    def setUp(self) -> None:
        self.indexer = ImagesIndexer("C:\\SolarImages")

    def test_is_exist_images_by_channel(self):
        message = "is_exist_images_by_channes_test() of Images Indexer not working"
        self.assertEqual(True, self.indexer.isExistImagesInChannel(94), message)

if __name__ == "__main__":
    main()