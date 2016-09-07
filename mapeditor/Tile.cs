using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Media.Imaging;
using System.Threading.Tasks;

namespace MapEditor
{
    public class Tile
    {
        public Tile(string id, string name, string imagePath)
        {
            BitmapImage thumbnail = new BitmapImage();
            thumbnail.BeginInit();
            thumbnail.UriSource = new Uri(imagePath, UriKind.Absolute);
            thumbnail.EndInit();
            this.Thumbnail = thumbnail;
            this.ID = id;
            this.Label = name;
        }

        public MagicBitmap Image { get; set; }
        public string ID { get; set; }
        public System.Windows.Media.ImageSource Thumbnail { get; set; }
        public string Label { get; set; }
    }
}
