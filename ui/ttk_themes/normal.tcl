namespace eval ttk::theme::normal {

    variable colors
    array set colors {
        -bg             "#f5f6f7"
        -fg             "#5c616c"
        -tv_bg          "#f0f0f7"
        -tv_bg_select   "#DFDFEF"
        -tv_fg          "gray30"
        -tv_fg_select   "#5295e2"
    }

    #___

    font configure TkDefaultFont -family calibri -size 10

    font create font -family calibri -size 10
    font create font_small -family calibri -size 8

    #___

    proc LoadImages {imgdir} {
        variable I
        foreach file [glob -directory $imgdir *.png] {
            set img [file tail [file rootname $file]]
            set I($img) [image create photo -file $file]
        }
    }

    LoadImages [file join [file dirname [info script]] normal]

    #__________________________________________________

    ttk::style theme create normal -parent default -settings {
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -font font \
            -borderwidth 0

        #___

        ttk::style element create Horizontal.Scale.trough \
            image [list $I(timeline-trough)] \
            -sticky nsew -border {8 5 8 5} -padding 0

        ttk::style element create Horizontal.Scale.slider \
            image [list $I(timeline-slider) \
                pressed $I(timeline-slider-pressed) \
                active $I(timeline-slider-active)] \
            -sticky nsew

        #___

        ttk::style configure TSeparator \
            -background $colors(-bg)

        #___

        ttk::style layout Treeview {
            Treeview.treearea -sticky nsew
        }

        ttk::style layout Treeview.Item {
            Treeitem.padding -sticky nswe -children {
                Treeitem.image -side left -sticky {}
                Treeitem.text -side left -sticky {}
            }
        }

        ttk::style configure Treeview \
            -rowheight 25 \
            -font font \
            -background $colors(-tv_bg) \
            -foreground $colors(-tv_fg)

        ttk::style map Treeview \
            -background [list selected $colors(-tv_bg_select)] \
            -foreground [list selected $colors(-tv_fg_select)]

        #___

        ttk::style layout Vertical.TScrollbar {
            Vertical.Scrollbar.trough -sticky ns -children {
                Vertical.Scrollbar.thumb -expand true
            }
        }

        ttk::style element create Vertical.Scrollbar.thumb \
            image [list $I(scrollbar-slider) \
                pressed $I(scrollbar-slider-pressed) \
                active $I(scrollbar-slider-active)] \
            -sticky ns -border 6

        #___

        ttk::style element create Entry.field \
            image [list $I(entry-border) \
                focus $I(entry-border-active) \
                hover $I(entry-border-active)] \
            -sticky nsew -border 3 -padding {6 4}

        #___

        ttk::style layout TMenubutton {
            Menubutton.button -children {
                Menubutton.focus -children {
                    Menubutton.padding -children {
                        Menubutton.indicator -side right
                        Menubutton.label -side right -expand true
                    }
                }
            }
        }

        ttk::style element create Menubutton.button \
            image [list $I(menubutton-btn) \
                pressed  $I(menubutton-btn-pressed) \
                active   $I(menubutton-btn-active)] \
            -sticky news -border 3 -padding {3 2}

        ttk::style element create Menubutton.indicator \
            image [list $I(menubutton-arrow) \
                pressed  $I(menubutton-arrow-active) \
                active   $I(menubutton-arrow-active)] \
            -sticky e -width 20

        ttk::style configure TMenubutton \
            -padding {8 4 4 4}

        #___

        ttk::style configure TLabel \
            -background $colors(-bg) \
    }
}