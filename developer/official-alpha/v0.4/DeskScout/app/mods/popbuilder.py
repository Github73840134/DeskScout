from win32more.Microsoft.UI.Xaml import Window, FrameworkElement
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop,Imaging,FontFamily,CompositionTarget,VisualTreeHelper
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Windows.UI.Xaml.Interop import TypeKind
from win32more.Windows.UI.Xaml import GridLength, GridLengthHelper, GridUnitType,DependencyObject,Thickness,Visibility
from win32more.Microsoft.UI.Xaml.Controls import Primitives,ToggleSplitButton,Border,ToggleSwitch,Page,HyperlinkButton,Button,CheckBox,ComboBox,NumberBox, ProgressRing,Image,PasswordBox,TextBlock,TextBox, Slider, StackPanel, NavigationView, Frame, NavigationViewItem, RowDefinition, Grid, GridView, GroupStyle, Canvas, ToolTip
class ContentType:
	plaintext=0x00
	xaml=0x01

def ok(content,ctype=ContentType.plaintext):
	if ctype == ContentType.plaintext:
		return XamlReader().Load(f"""<Page
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
      xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
      xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
      xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
	<StackPanel>
		<TextBlock Text="{content}"/>
		<Button Name="popup.content.ok" Content="OK"/>
	</StackPanel>
</Page>""")
def yesno(content,ctype=ContentType.plaintext):
	if ctype == ContentType.plaintext:
		return XamlReader().Load(f"""<Page
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
      xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
      xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
      xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006">
	<StackPanel>
		<TextBlock Text="{content}"/>
		<StackPanel Orientation="Horizontal"/>
			<Button Name="popup.content.yes" Content="yes"/>
			<Button Name="popup.content.no" Content="no"/>
		</StackPanel>
	</StackPanel>
</Page>""")
def progress(content,progress,isDeterminate=False,ctype=ContentType.plaintext):
	if ctype == ContentType.plaintext:
		return XamlReader().Load(f"""<Page
xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation">
			<StackPanel Orientation="Horizontal">
				<ProgressRing Value="{progress}" IsIndeterminate="{str(not isDeterminate)}"/>
				<TextBlock Margin="5,0,0,0" Text="{content}" Name="popup.content.loading_status"/>
			</StackPanel>
	
</Page>""")
	