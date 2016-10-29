using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MapEditor
{
    class Util
    {
        private static string gitRoot = null;
        public static string GetGitRoot()
        {
            if (gitRoot == null)
            {
                string walker = System.IO.Directory.GetCurrentDirectory();
                while (!System.IO.File.Exists(System.IO.Path.Combine(walker, "Platformer.build")))
                {
                    walker = System.IO.Path.GetDirectoryName(walker);
                }
                gitRoot = walker;
            }
            return gitRoot;
        }
    }
}
