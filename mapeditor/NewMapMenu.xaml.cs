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
    /// Interaction logic for NewMapMenu.xaml
    /// </summary>
    public partial class NewMapMenu : Window
    {
        public NewMapMenu()
        {
            InitializeComponent();
            this.map_width.Text = "20";
            this.map_height.Text = "15";
            this.ok_button.Click += Ok_button_Click;
            this.map_width.Focus();
        }

        private void Ok_button_Click(object sender, RoutedEventArgs e)
        {
            string widthText = this.map_width.Text;
            string heightText = this.map_height.Text;
            int width, height;
            if (int.TryParse(widthText, out width) && int.TryParse(heightText, out height))
            {
                MainWindow.Instance.CreateNewMap(width, height);
                this.Close();
            }
            else
            {
                System.Windows.MessageBox.Show("Width and height invalid.");
            }
        }
    }
}
