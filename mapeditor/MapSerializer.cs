using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MapEditor
{
    class MapSerializer
    {
        private Map map;

        public MapSerializer(Map map)
        {
            this.map = map;
        }

        public string Serialize()
        {
            Dictionary<string, string> values = new Dictionary<string, string>();
            int width = map.Width;
            int height = map.Height;
            //values["width"] = width + "";
            //values["height"] = height + "";

            List<string> tileStringBuilder = new List<string>();
            Tile tile;
            Tile[,] tiles = map.Tiles;
            for (int y = 0; y < height; ++y)
            {
                for (int x = 0; x < width; ++x)
                {
                    tile = tiles[x, y];
                    if (tile == null)
                    {
                        tileStringBuilder.Add(".");
                    }
                    else
                    {
                        tileStringBuilder.Add(tile.ID);
                    }
                }
                tileStringBuilder.Add("\n");
            }

            values["tiles"] = string.Join("", tileStringBuilder).Trim();
            
            List<string> output = new List<string>();
            foreach (string key in values.Keys.OrderBy(k => k.ToLower()))
            {
                string value = values[key];
                if (value.Contains("\n"))
                {
                    output.Add("#" + key);
                    output.Add(value);
                }
                else
                {
                    output.Add("#" + key + ":" + value);
                }
            }

            return string.Join("\n", output);
        }
    }
}
