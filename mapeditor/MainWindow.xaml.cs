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
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public static MainWindow Instance = null;

        private Map _activeDocument = null;
        public Map ActiveDocument
        {
            get { return this._activeDocument; }
            set
            {
                this._activeDocument = value;
                this.tileBoard.ClearMapCache();
            }
        }

        public bool IsKeyPressed(string id)
        {
            return this.keysPressed.ContainsKey(id) && this.keysPressed[id];
        }

        private Dictionary<string, bool> keysPressed = new Dictionary<string, bool>();

        public MainWindow()
        {
            Instance = this;

            InitializeComponent();

            this.Loaded += MainWindow_Loaded;
            EventManager.RegisterClassHandler(typeof(Window), Keyboard.KeyUpEvent, new KeyEventHandler(this.KeyUpHandler), true);
            EventManager.RegisterClassHandler(typeof(Window), Keyboard.KeyDownEvent, new KeyEventHandler(this.KeyDownHandler), true);
        }

        private void KeyUpHandler(object sender, KeyEventArgs e) { this.KeyDownUpHandler(e.Key, false); }
        private void KeyDownHandler(object sender, KeyEventArgs e) { this.KeyDownUpHandler(e.Key, true); }

        private void KeyDownUpHandler(Key key, bool down)
        {
            string id = key.ToString().ToLower();
            switch (key)
            {
                case Key.LeftShift: id = "shift"; break;
                case Key.RightShift: id = "shit"; break;
                case Key.LeftCtrl: id = "ctrl"; break;
                case Key.RightCtrl: id = "ctrl"; break;
                default: break;
            }
            this.keysPressed[id] = down;

            if (down)
            {
                string shortcutPattern =
                    (this.IsKeyPressed("ctrl") ? "ctrl+" : "") +
                    (this.IsKeyPressed("shift") ? "shift+" : "") +
                    id;
                switch (shortcutPattern)
                {
                    case "ctrl+n": this.MenuItem_New(this, null); break;
                    case "ctrl+o": this.MenuItem_Open(this, null); break;
                    case "ctrl+s": this.MenuItem_Save(this, null); break;
                    case "ctrl+e": this.MenuItem_Resize(this, null); break;
                    default: break;
                }
            }
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            this.palette.ItemsSource = TileStore.GetTiles();
        }

        // Prompts a save if document dirty
        // Returns true if whatever you are doing should continue (false returned if user cancels save.
        private bool PromptSaveIfNecessaryAndMaybeContinue()
        {
            if (this.ActiveDocument != null && this.ActiveDocument.IsDirty)
            {
                MessageBoxResult result = System.Windows.MessageBox.Show("Save changes?", "Hi", MessageBoxButton.YesNoCancel);
                if (result == MessageBoxResult.Cancel)
                {
                    return false;
                }

                if (result == MessageBoxResult.Yes)
                {
                    return this.SaveImpl();
                }

                if (result == MessageBoxResult.No)
                {
                    return true;
                }

                throw new Exception();
            }
            return true;
        }

        private void MenuItem_Resize(object sender, RoutedEventArgs e)
        {
            if (this.ActiveDocument == null) return;
            int width = this.ActiveDocument.Width;
            int height = this.ActiveDocument.Height;
            ResizeMenu menu = new ResizeMenu(width, height);
            menu.Owner = this;
            menu.ShowDialog();
        }

        public void ResizeDocument(int newWidth, int newHeight, bool anchorLeft, bool anchorTop)
        {
            if (this.ActiveDocument.Width == newWidth && this.ActiveDocument.Height == newHeight) return;

            Tile[,] sourceTiles = this.ActiveDocument.Tiles;
            Tile[,] targetTiles = new Tile[newWidth, newHeight];

            int sourceLeft = 0;
            int sourceWidth = this.ActiveDocument.Width;
            int targetWidth;
            int targetLeft;
            if (newWidth > sourceWidth)
            {
                targetWidth = sourceWidth;
                targetLeft = anchorLeft ? 0 : (newWidth - sourceWidth);
            }
            else
            {
                sourceLeft = anchorLeft ? 0 : (sourceWidth - newWidth);
                sourceWidth = newWidth;
                targetWidth = newWidth;
                targetLeft = 0;
            }

            int sourceTop = 0;
            int sourceHeight = this.ActiveDocument.Height;
            int targetHeight;
            int targetTop;
            if (newHeight > sourceHeight)
            {
                targetHeight = sourceHeight;
                targetTop = anchorTop ? 0 : (newHeight - sourceHeight);
            }
            else
            {
                sourceTop = anchorTop ? 0 : (sourceHeight - newHeight);
                sourceHeight = newHeight;
                targetHeight = newHeight;
                targetTop = 0;
            }

            int targetX, sourceX, targetY, sourceY;
            sourceY = sourceTop;
            targetY = targetTop;
            for (int y = 0; y < sourceHeight; ++y)
            {
                sourceX = sourceLeft;
                targetX = targetLeft;
                for (int x = 0; x < sourceWidth; ++x)
                {
                    targetTiles[targetX, targetY] = sourceTiles[sourceX, sourceY];
                    sourceX++;
                    targetX++;
                }
                sourceY++;
                targetY++;
            }

            this.ActiveDocument.Tiles = targetTiles;
            this.ActiveDocument.Width = newWidth;
            this.ActiveDocument.Height = newHeight;
            this.ActiveDocument.IsDirty = true;
            this.tileBoard.ForceRefresh();
            this.RefreshDisplayTitle();
        }

        private void MenuItem_New(object sender, RoutedEventArgs e)
        {
            if (this.PromptSaveIfNecessaryAndMaybeContinue())
            {
                new NewMapMenu().ShowDialog();
            }
        }

        private void MenuItem_Open(object sender, RoutedEventArgs e)
        {
            if (this.PromptSaveIfNecessaryAndMaybeContinue())
            {
                System.Windows.Forms.OpenFileDialog ofd = new System.Windows.Forms.OpenFileDialog();
                System.Windows.Forms.DialogResult result = ofd.ShowDialog();
                switch (result)
                {
                    case System.Windows.Forms.DialogResult.OK:
                        string path = ofd.FileName;
                        if (System.IO.File.Exists(path))
                        {
                            this.ActiveDocument = new Map(path);
                            this.RefreshDisplayTitle();
                            this.tileBoard.ForceRefresh();
                        }
                        break;
                    case System.Windows.Forms.DialogResult.Cancel:
                        break;
                    default:
                        throw new Exception();
                }
            }
        }

        private void MenuItem_Save(object sender, RoutedEventArgs e)
        {
            if (this.ActiveDocument != null && this.ActiveDocument.IsDirty)
            {
                this.SaveImpl();
            }
        }

        private bool SaveImpl()
        {
            if (this.ActiveDocument == null) return false;

            if (this.ActiveDocument.Path == null)
            {
                System.Windows.Forms.SaveFileDialog sfd = new System.Windows.Forms.SaveFileDialog();

                System.Windows.Forms.DialogResult result = sfd.ShowDialog();
                switch (result)
                {
                    case System.Windows.Forms.DialogResult.OK:
                        break;
                    case System.Windows.Forms.DialogResult.Cancel:
                        return false;
                    default:
                        throw new Exception();
                }

                string filename = sfd.FileName;
                this.ActiveDocument.Path = filename;
            }

            string mapContent = new MapSerializer(this.ActiveDocument).Serialize();
            System.IO.File.WriteAllText(this.ActiveDocument.Path, mapContent);
            this.ActiveDocument.IsDirty = false;
            this.RefreshDisplayTitle();

            return true;
        }

        public void CreateNewMap(int width, int height)
        {
            this.ActiveDocument = new Map(width, height);

            this.RefreshDisplayTitle();
            this.tileBoard.ForceRefresh();

        }

        public void RefreshDisplayTitle()
        {
            this.Title = this.ActiveDocument.DisplayTitle;
        }

        private void TileBoard_SizeChanged(object sender, SizeChangedEventArgs e)
        {

        }

        public Tile ActiveBrush
        {
            get
            {
                return this.palette.SelectedValue as Tile;
            }
            set
            {
                this.palette.SelectedValue = value;
            }
        }
    }
}
