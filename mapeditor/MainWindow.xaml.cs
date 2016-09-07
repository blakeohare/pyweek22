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

        private Dictionary<string, bool> keysPressed = new Dictionary<string, bool>()
        {
            { "space", false },
            { "shift", false },
        };

        public MainWindow()
        {
            Instance = this;

            InitializeComponent();

            this.Loaded += MainWindow_Loaded;
            this.KeyDown += (sender, e) => { this.KeyDownUpHandler(e.Key, true); };
            this.KeyUp += (sender, e) => { this.KeyDownUpHandler(e.Key, false); };
            EventManager.RegisterClassHandler(typeof(Window), Keyboard.KeyUpEvent, new KeyEventHandler(this.KeyUpHandler), true);
            EventManager.RegisterClassHandler(typeof(Window), Keyboard.KeyDownEvent, new KeyEventHandler(this.KeyDownHandler), true);
        }

        private void KeyUpHandler(object sender, KeyEventArgs e) { this.KeyDownUpHandler(e.Key, false); }
        private void KeyDownHandler(object sender, KeyEventArgs e) { this.KeyDownUpHandler(e.Key, true); }

        private void KeyDownUpHandler(Key key, bool down)
        {
            switch (key)
            {
                case Key.Space: this.keysPressed["space"] = down; break;
                case Key.LeftShift: this.keysPressed["shift"] = down; break;
                case Key.RightShift: this.keysPressed["shift"] = down; break;
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
