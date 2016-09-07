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
        
        public Map ActiveDocument { get; set; }

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

        private void MenuItem_New(object sender, RoutedEventArgs e)
        {
            if (this.ActiveDocument != null && this.ActiveDocument.IsDirty)
            {
                MessageBoxResult result = System.Windows.MessageBox.Show("Save changes?", "Hi", MessageBoxButton.YesNoCancel);
                if (result == MessageBoxResult.Cancel) return;
                if (result == MessageBoxResult.Yes)
                {
                    // TODO: save
                }
            }
            new NewMapMenu().ShowDialog();
        }

        public void CreateNewMap(int width, int height)
        {
            this.ActiveDocument = new Map(width, height);
            this.RefreshDisplayTitle();
            this.tileBoard.Refresh();
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
