import yahoo
import urllib2
from yahoo.search.image import ImageSearch
import matplotlib.pyplot as plt
from mpl_figure_editor import MPLFigureEditor
from matplotlib.figure import Figure
from enthought.traits.api import HasTraits, Str, Int, Float, Enum,DelegatesTo,This,Instance, Button
from enthought.traits.ui.wx.editor import Editor
from enthought.traits.ui.api import *#View, Item, Group, ButtonEditor
import ImageFilter
import Image

class Viewer(HasTraits):
    """
    When I instantiate the Viewer class, the following triats are defined.
    To view the GUI, call the configure_triats method.
    """
    query = Str
    url = Str
    decolor = Button()
    update = Button()
    contour = Button()
    blur = Button()
    edges = Button()
    

    figure  = Instance(Figure, ())
    view = View(Item('url'),
                Item('query'),
                Item('update',show_label=False),
                Item('figure', editor=MPLFigureEditor(),
                     show_label=False),
                Group(Item('decolor',show_label=False),
                      Item('contour',show_label=False),
                      Item('blur',show_label=False),
                      Item('edges',show_label=False),
                      label='Image Manipulation)',dock='horizontal'),
                width=600,height=800,resizable=True)
    

    def display(self):
        """
        The Display method.  This redisplays what ever image file is in im.
        It is called at the end of each image manipulation function.
        """

        axis = self.figure.add_subplot(111)
        axis.imshow(self.im)
        self.figure.canvas.draw()




    def getimage(self,query):
        """
        Uses the yahoo module to run a Yahoo image search.  It reads the
        linked image as a hex string.  Then it saves it into a temporary file
        and reads it back using Image.open.  It then displays the image.
        """
        srch = ImageSearch(app_id="YahooDemo", query=self.query,results=1)


        for a in srch.parse_results():
            url = a.Url
            imstring = urllib2.urlopen(url).read()
            output = open('temp.jpg','wb')
            output.write(imstring)
            output.close()
        

        self.url = url
        self.im = Image.open('temp.jpg')
        self.im = self.im.rotate(180)
        self.display()

    def _update_fired(self):
        """
        After we are finished typing in the query, then call getimage.  If we
        instead call get image each time we query is changed, it will run a new
        search on every new character.
        """

        self.getimage(self.query)        


    #The image manipulation buttons.  They just use the canned functionality
    #of the Image module

    def _decolor_fired(self):
        r,g,b = self.im.split()
        self.im = Image.merge("RGB", (g,g,g))
        self.display()

    def _contour_fired(self):
        self.im = self.im.filter(ImageFilter.CONTOUR)
        self.display()

    def _blur_fired(self):
        self.im = self.im.filter(ImageFilter.BLUR)
        self.display()

    def _edges_fired(self):
        self.im = self.im.filter(ImageFilter.FIND_EDGES)
        self.display()

