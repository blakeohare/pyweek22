using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MapEditor
{
    public class Map
    {
        public string Path { get; set; }
        public bool IsDirty { get; set; }
        public int Width { get; set; }
        public int Height { get; set; }
        private Dictionary<string, string> rawValues;
        public Tile[,] Tiles { get; set; }
        
        public Map(int width, int height)
        {
            this.Width = width;
            this.Height = height;
            this.Tiles = new Tile[width, height];
            this.IsDirty = true;
            this.Path = null;
            this.rawValues = new Dictionary<string, string>();        }

        public Map(string path)
        {
            this.Path = path;
            this.IsDirty = false;
            MapParser parser = new MapParser(path);
            this.Width = parser.Width;
            this.Height = parser.Height;
            this.Tiles = parser.Tiles;
        }

        public string DisplayTitle
        {
            get
            {
                return (this.IsDirty ? "* " : "") + (this.Path ?? "Untitled Map") + " (" + this.Width + " x " + this.Height + ")";
            }
        }
    }
}
