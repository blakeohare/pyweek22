using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Media.Imaging;
using System.Windows.Media;
using System.Threading.Tasks;

namespace MapEditor
{
    /// <summary>
    /// Encapsulates a WriteableBitmap.
    /// </summary>
    public class MagicBitmap
    {
        private WriteableBitmap systemBitmap;
        private uint[] pixels;

        public ImageSource ImageSource { get { return this.systemBitmap; } }
        public int Width { get; set; }
        public int Height { get; set; }


        public MagicBitmap(string path)
        {
            BitmapImage thumbnail = new BitmapImage();
            thumbnail.BeginInit();
            thumbnail.UriSource = new Uri(path, UriKind.Absolute);
            thumbnail.EndInit();
            this.systemBitmap = new WriteableBitmap(thumbnail);
            this.Width = this.systemBitmap.PixelWidth;
            this.Height = this.systemBitmap.PixelHeight;
            this.pixels = new uint[this.Width * this.Height];
            byte[] bytes = new byte[64 * 4];
            System.Windows.MessageBox.Show("A");
            this.systemBitmap.Lock();
            this.systemBitmap.CopyPixels(new System.Windows.Int32Rect(0, 0, this.Width, this.Height), this.pixels, this.Width * 4, 0);
            //this.systemBitmap.CopyPixels(bytes, this.Width * 4, 0);
            this.systemBitmap.Unlock();
            System.Windows.MessageBox.Show("B");
        }

        public MagicBitmap(int width, int height)
        {
            this.Width = width;
            this.Height = height;
            this.systemBitmap = new WriteableBitmap(width, height, 96, 96, PixelFormats.Bgra32, null);
            this.pixels = new uint[this.Width * this.Height];
        }

        private static uint GetUIntColor(byte r, byte g, byte b)
        {
            uint red = r;
            uint green = g;
            uint blue = b;
            return (blue << 24) | (green << 16) | (red << 8) | 255;
        }

        public void SetTransparentColor(byte r, byte g, byte b)
        {
            uint color = GetUIntColor(r, g, b);
            uint[] pixels = this.pixels;
            int i = pixels.Length;
            while (i-- > 0)
            {
                if (pixels[i] == color)
                {
                    pixels[i] = 0;
                }
            }
        }

        public void Fill(byte r, byte g, byte b)
        {
            uint color = GetUIntColor(r, g, b);
            uint[] pixels = this.pixels;
            int i = pixels.Length;
            while (i-- > 0)
            {
                pixels[i] = color;
            }
        }

        public void Blit(MagicBitmap source, int targetX, int targetY)
        {
            int sourceX = 0;
            int sourceY = 0;
            int width = source.Width;
            int height = source.Height;
            if (targetX >= this.Width) return;
            if (targetY >= this.Height) return;
            if (targetX + width < 0) return;
            if (targetY + height < 0) return;
            if (targetX < 0)
            {
                int leftOverhang = -targetX;
                sourceX = leftOverhang;
                width -= leftOverhang;
            }
            if (targetY < 0)
            {
                int topOverhang = -targetY;
                sourceY = topOverhang;
                height -= topOverhang;
            }
            if (targetX + width > this.Width)
            {
                int rightOverhang = targetX + width - this.Width;
                width -= rightOverhang;
            }
            if (targetY + height > this.Height)
            {
                int bottomOverhang = targetY + height - this.Height;
                height -= bottomOverhang;
            }

            uint[] sourcePixels = source.pixels;
            uint[] targetPixels = this.pixels;
            int sourceIndex, targetIndex;
            int x;
            uint sourceColor;
            uint alpha;
            for (int y = 0; y < height; ++y)
            {
                sourceIndex = sourceY * source.Width + sourceX;
                targetIndex = targetY * this.Width + targetY;
                x = width;
                while (x-- > 0)
                {
                    sourceColor = sourcePixels[sourceIndex++];
                    alpha = sourceColor & 255;
                    if (alpha == 0)
                    {
                        targetIndex++;
                    }
                    else // TODO: non boolean alphas
                    {
                        targetPixels[targetIndex++] = sourceColor;
                    }
                }
            }
        }

        public void FlushChanges()
        {
            this.systemBitmap.Lock();
            this.systemBitmap.WritePixels(new System.Windows.Int32Rect(0, 0, this.Width, this.Height), this.pixels, this.Width * 4, 0);
            this.systemBitmap.Unlock();
        }
    }
}
