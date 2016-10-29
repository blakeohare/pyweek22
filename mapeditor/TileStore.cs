using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MapEditor
{
    public static class TileStore
    {
        private static string[] tiles = null;
        private static Dictionary<string, Tile> idsToTiles = new Dictionary<string, Tile>();
        private static Dictionary<string, string> idsToPaths = new Dictionary<string, string>();
        private static void Init()
        {
            if (tiles != null) return;

            string gitRoot = Util.GetGitRoot();
            string manifestPath = System.IO.Path.Combine(gitRoot, "source", "images", "tiles", "manifest.txt");
            foreach (string line in System.IO.File.ReadAllLines(manifestPath))
            {
                string trimmedLine = line.Trim();
                if (trimmedLine.Length > 0 && trimmedLine[0] != '#')
                {
                    string[] parts = trimmedLine.Split('\t');
                    string id = parts[0];
                    string flags = parts[1];
                    string imagePath = parts[2].Split(',')[0];
                    Tile tile = new Tile(id, imagePath, System.IO.Path.Combine(gitRoot, "source", "images", "tiles", (imagePath + ".png").Replace('/', '\\')));
                    idsToTiles[id] = tile;
                    idsToPaths[id] = imagePath;
                }
            }

            List<string> ids = new List<string>(idsToTiles.Keys);
            TileStore.tiles = ids.OrderBy(id => idsToPaths[id]).ToArray();
        }

        public static List<Tile> GetTiles()
        {
            Init();
            List<Tile> tiles = new List<Tile>(TileStore.tiles.Select<string, Tile>(tileId => idsToTiles[tileId]));
            return tiles;
        }

        public static Tile GetTile(string id)
        {
            if (id == null || id.Length == 0) return null;
            return idsToTiles[id];
        }
    }
}
