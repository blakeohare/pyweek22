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
using System.Windows.Shapes;

namespace MapEditor
{
    /// <summary>
    /// Interaction logic for ResizeMenu.xaml
    /// </summary>
    public partial class ResizeMenu : Window
    {
        public ResizeMenu(int width, int height)
        {
            InitializeComponent();
            this.width_textbox.Text = width + "";
            this.height_textbox.Text = height + "";
            this.ok_button.Click += (sender, e) =>
            {
                int newWidth, newHeight;
                if (int.TryParse(this.width_textbox.Text, out newWidth) &&
                    int.TryParse(this.height_textbox.Text, out newHeight) &&
                    newWidth > 1 &&
                    newHeight > 1)
                {
                    string anchor = this.anchor_combobox.SelectionBoxItem as string ?? "Top-Left";
                    anchor = anchor.ToLower();
                    bool anchorLeft = anchor.EndsWith("-left");
                    bool anchorTop = anchor.StartsWith("top-");
                    MainWindow.Instance.ResizeDocument(newWidth, newHeight, anchorLeft, anchorTop);
                    this.Close();
                    return;
                }
                System.Windows.MessageBox.Show("Size parameters invalid.");
            };
        }
    }
}
