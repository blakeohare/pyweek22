using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace MapEditor
{
    /// <summary>
    /// Interaction logic for TileBoard.xaml
    /// </summary>
    public partial class TileBoard : UserControl
    {
        private int xOffset = 0;
        private int yOffset = 0;
        private int lastMouseX = 0;
        private int lastMouseY = 0;

        private enum CursorState
        {
            NONE,
            DRAW, // left click/drag
            ERASE, // shift + left click/drag
            DROPPER, // rigth click/drag
            PAN, // space + left click/drag
        }

        private CursorState cursorState = CursorState.NONE;
        private Map _map = null;

        public Map Map
        {
            get
            {
                if (this._map == null)
                {
                    this._map = MainWindow.Instance.ActiveDocument;
                }
                return this._map;
            }
        }

        private List<Image> members = new List<Image>();

        public TileBoard()
        {
            InitializeComponent();
            this.mouse_catcher.MouseDown += this.MouseDownHandler;
            this.mouse_catcher.MouseUp += this.MouseUpHandler;
            this.mouse_catcher.MouseMove += this.MouseMoveHandler;
        }

        public void Refresh()
        {
            if (!this.isUiDirty)
            {
                return;
            }

            this.isUiDirty = false;

            if (this.Map == null)
            {
                this.members.Clear();
                this.tile_host.Children.Clear();
                this.backdrop.Visibility = Visibility.Collapsed;
            }
            else
            {
                int width = this.Map.Width;
                int height = this.Map.Height;

                this.backdrop.Visibility = Visibility.Visible;
                this.backdrop.Width = width * 32;
                this.backdrop.Height = height * 32;
                this.backdrop.Margin = new Thickness(this.xOffset, this.yOffset, 0, 0);

                int membersIndex = 0;
                Tile tile;
                UIElementCollection tileHostChildren = this.tile_host.Children;
                Image image;
                Tile[,] tiles = this.Map.Tiles;
                for (int y = 0; y < height; ++y)
                {
                    for (int x = 0; x < width; ++x)
                    {
                        tile = tiles[x, y];
                        if (tile != null)
                        {
                            if (membersIndex == this.members.Count)
                            {
                                image = new Image()
                                {
                                    HorizontalAlignment = HorizontalAlignment.Left,
                                    VerticalAlignment = VerticalAlignment.Top
                                };

                                RenderOptions.SetBitmapScalingMode(image, BitmapScalingMode.NearestNeighbor);
                                this.members.Add(image);
                                tileHostChildren.Add(image);
                            }

                            image = this.members[membersIndex++];
                            image.Width = 32;
                            image.Height = 32;
                            image.Margin = new Thickness(this.xOffset + x * 32, this.yOffset + y * 32, 0, 0);
                            image.Source = tile.Thumbnail;
                        }
                    }
                }

                int oldLength = this.members.Count;
                for (int i = membersIndex; i < oldLength; ++i)
                {
                    this.members.RemoveAt(this.members.Count - 1);
                    tileHostChildren.RemoveAt(tileHostChildren.Count - 1);
                }
            }
        }

        private static int[] COORD = new int[2];

        public bool CalculateCoordinate(int pixelX, int pixelY)
        {
            int x = pixelX - xOffset;
            int y = pixelY - yOffset;
            if (x < 0 || y < 0) return false;
            Map map = MainWindow.Instance.ActiveDocument;
            if (map == null) return false;
            int col = x / 32;
            int row = y / 32;
            if (col >= map.Width) return false;
            if (row >= map.Height) return false;
            COORD[0] = col;
            COORD[1] = row;
            return true;
        }

        private void MouseMoveHandler(object sender, MouseEventArgs e)
        {
            Point p = e.GetPosition(this);
            int cx = (int)p.X;
            int cy = (int)p.Y;
            bool onBoard = this.CalculateCoordinate(cx, cy);
            int col = COORD[0];
            int row = COORD[1];

            switch (this.cursorState)
            {
                case CursorState.NONE:
                    break;

                case CursorState.DRAW:
                    if (onBoard)
                    {
                        this.ApplyBrush(col, row, MainWindow.Instance.ActiveBrush);
                    }
                    break;

                case CursorState.DROPPER:
                    if (onBoard)
                    {
                        if (this.Map != null)
                        {
                            MainWindow.Instance.ActiveBrush = this.Map.Tiles[col, row];
                        }
                    }
                    break;

                case CursorState.ERASE:
                    if (onBoard)
                    {
                        this.ApplyBrush(col, row, null);
                    }
                    break;

                case CursorState.PAN:
                    this.xOffset += (cx - this.lastMouseX);
                    this.yOffset += (cy - this.lastMouseY);
                    this.isUiDirty = true;
                    break;

                default:
                    throw new Exception();
            }
            this.lastMouseX = cx;
            this.lastMouseY = cy;

            this.Refresh();
        }

        private bool isUiDirty = false;

        private void MouseUpHandler(object sender, MouseButtonEventArgs e)
        {
            this.mouse_catcher.ReleaseMouseCapture();
            this.cursorState = CursorState.NONE;
        }

        private void MouseDownHandler(object sender, MouseButtonEventArgs e)
        {
            this.mouse_catcher.CaptureMouse();
            Point p = e.GetPosition(this);
            this.lastMouseX = (int)p.X;
            this.lastMouseY = (int)p.Y;

            if (e.ChangedButton == MouseButton.Left)
            {
                if (MainWindow.Instance.IsKeyPressed("space"))
                {
                    this.cursorState = CursorState.PAN;
                }
                else if (MainWindow.Instance.IsKeyPressed("shift"))
                {
                    this.cursorState = CursorState.ERASE;
                    this.MouseMoveHandler(sender, e);
                }
                else
                {
                    this.cursorState = CursorState.DRAW;
                    this.MouseMoveHandler(sender, e);
                }
            }
            else if (e.ChangedButton == MouseButton.Right)
            {
                this.cursorState = CursorState.DROPPER;
                this.MouseMoveHandler(sender, e);
            }
            else
            {
                this.cursorState = CursorState.NONE;
            }
        }
        
        private void ApplyBrush(int col, int row, Tile brush)
        {
            Tile tile = this.Map.Tiles[col, row];
            if (tile != brush)
            {
                this.Map.Tiles[col, row] = brush;
                this.isUiDirty = true;
            }
        }
    }
}
