using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MapEditor
{
    class MapParser
    {
        public Dictionary<string, string> RawValues { get; set; }
        public int Width { get; set; }
        public int Height { get; set; }
        public Tile[,] Tiles { get; set; }

        public MapParser (string path)
        {
            string[] rawLines = System.IO.File.ReadAllLines(path);
            Dictionary<string, string> rawValues = new Dictionary<string, string>();
            foreach (string line in rawLines)
            {
                string trimmedLine = line.Trim();
                if (trimmedLine.Length > 0)
                {
                    string[] parts = line.Split(':');
                    string key = parts[0].Trim().ToLower();
                    List<string> valueBuilder = new List<string>();
                    for (int i = 1; i < parts.Length; ++i)
                    {
                        valueBuilder.Add(parts[i]);
                    }
                    string value = string.Join(":", valueBuilder);
                    rawValues[key] = value;
                }
            }

            string[] tileIds = rawValues["tiles"].Split(',');

            this.Width = int.Parse(rawValues["width"]);
            this.Height = int.Parse(rawValues["height"]);
            this.Tiles = new Tile[this.Width, this.Height];
            int index = 0;
            string id;
            for (int y = 0; y < this.Height; ++y)
            {
                for (int x = 0; x < this.Width; ++x)
                {
                    id = tileIds[index++].Trim();
                    if (id.Length > 0)
                    {
                        this.Tiles[x, y] = TileStore.GetTile(id);
                    }
                }
            }
        }
    }
}
