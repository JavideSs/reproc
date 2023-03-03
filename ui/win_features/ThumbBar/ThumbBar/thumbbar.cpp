#include "Python.h"
#include "ShObjIdl_core.h"  //ITaskbarList3
#include "strsafe.h"        //StringCchCopy()

#include <iostream>

#define IDTB_BTN_PREVIOUS   0001
#define IDTB_BTN_PLAYPAUSE  0002
#define IDTB_BTN_NEXT       0003

#define RELPATH L"ui\\win_features\\ThumbBar\\images\\"
#define IMGPATH_BTN96  RELPATH"TBbtns96.bmp"
#define IMGPATH_BTN120 RELPATH"TBbtns120.bmp"
#define IMGPATH_BTN144 RELPATH"TBbtns144.bmp"

#define HOVERTEXT_BTN_PREVIOUS  L"Previous"
#define HOVERTEXT_BTN_PLAY      L"Play"
#define HOVERTEXT_BTN_PAUSE     L"Pause"
#define HOVERTEXT_BTN_NEXT      L"Next"

HWND hWnd;
WNDPROC wndproc_tk;
PyObject* pFuncs[4];

//https://docs.microsoft.com/es-es/windows/win32/shell/taskbar-extensions
//https://github.com/microsoft/Windows-classic-samples/blob/main/Samples/Win7Samples/winui/shell/appshellintegration/TaskbarThumbnailToolbar/ThumbnailToolbar.cpp

//==================================================

HIMAGELIST himl;

struct BitMap{
    LPCWSTR pbmp;
    int cx;
};

HIMAGELIST createImageList(){

    const BitMap btns_data[3] = {
        {IMGPATH_BTN96, 16},
        {IMGPATH_BTN120, 20},
        {IMGPATH_BTN144, 24}
    };

    const int btn_system_cx = GetSystemMetrics(SM_CXSMICON);

    unsigned btns_data_i = 0;
    for (unsigned i = 0; i < ARRAYSIZE(btns_data); i++)
        if (btns_data[i].cx <= btn_system_cx)
            btns_data_i = i;

    return ImageList_LoadImage(
        NULL,
        btns_data[btns_data_i].pbmp,
        btns_data[btns_data_i].cx,
        0,
        CLR_NONE,
        IMAGE_BITMAP,
        LR_CREATEDIBSECTION | LR_LOADFROMFILE | LR_LOADTRANSPARENT
    );
}

//==================================================

ITaskbarList3* pTaskbarList;

const int btns_n = 3;
THUMBBUTTON btns[btns_n];

int is_song_playing = 0;

HRESULT ReleaseThumbnailToolbar(){

    ImageList_Destroy(himl);
    HRESULT hr = pTaskbarList->Release();

    return hr;
}

HRESULT CreateThumbnailToolbar(HWND hWnd){

    HRESULT hr = CoCreateInstance(
        CLSID_TaskbarList,
        NULL,
        CLSCTX_INPROC_SERVER,
        IID_PPV_ARGS(&pTaskbarList)
    );

    if (!SUCCEEDED(hr))
        return hr;

    hr = pTaskbarList->HrInit();
    if (!SUCCEEDED(hr)){
        pTaskbarList->Release();
        return hr;
    }

    himl = createImageList();
    if (!himl){
        pTaskbarList->Release();
        return hr;
    }

    hr = pTaskbarList->ThumbBarSetImageList(hWnd, himl);
    if (!SUCCEEDED(hr)){
        ImageList_Destroy(himl);
        pTaskbarList->Release();
        return hr;
    }

    //Previous Btn
    btns[0].dwMask = THB_BITMAP | THB_TOOLTIP | THB_FLAGS;
    btns[0].dwFlags = THBF_ENABLED;
    btns[0].iId = IDTB_BTN_PREVIOUS;
    btns[0].iBitmap = 0;
    StringCchCopy(btns[0].szTip, ARRAYSIZE(btns[0].szTip), HOVERTEXT_BTN_PREVIOUS);

    //Play Btn
    btns[1].dwMask = THB_BITMAP | THB_TOOLTIP | THB_FLAGS;
    btns[1].dwFlags = THBF_ENABLED;
    btns[1].iId = IDTB_BTN_PLAYPAUSE;
    btns[1].iBitmap = 1;
    StringCchCopy(btns[1].szTip, ARRAYSIZE(btns[1].szTip), HOVERTEXT_BTN_PLAY);

    //Next Btn
    btns[2].dwMask = THB_BITMAP | THB_TOOLTIP | THB_FLAGS;
    btns[2].dwFlags = THBF_ENABLED;
    btns[2].iId = IDTB_BTN_NEXT;
    btns[2].iBitmap = 3;
    StringCchCopy(btns[2].szTip, ARRAYSIZE(btns[2].szTip), HOVERTEXT_BTN_NEXT);

    hr = pTaskbarList->ThumbBarAddButtons(hWnd, btns_n, btns);

    return hr;
}

HRESULT UpdateThumbnailToolbar(int is_song_playing){

    if (is_song_playing){
        //Pause Btn
        btns[1].iBitmap = 2;
        StringCchCopy(btns[1].szTip, ARRAYSIZE(btns[1].szTip), HOVERTEXT_BTN_PAUSE);
    }
    else{
        //Play Btn
        btns[1].iBitmap = 1;
        StringCchCopy(btns[1].szTip, ARRAYSIZE(btns[1].szTip), HOVERTEXT_BTN_PLAY);
    }

    HRESULT hr = pTaskbarList->ThumbBarUpdateButtons(hWnd, btns_n, btns);

    return hr;
}

//==================================================

//Processes the message sent when a button is clicked
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam){

    switch (message){
        case WM_COMMAND:{
            PyGILState_STATE d_gstate = PyGILState_Ensure();
            switch (LOWORD(wParam)){
                case IDTB_BTN_PREVIOUS:{
                    PyObject_Call(pFuncs[0], PyTuple_New(0), NULL);
                    break;
                }
                case IDTB_BTN_PLAYPAUSE:{
                    PyObject_Call(is_song_playing ? pFuncs[2] : pFuncs[1], PyTuple_New(0), NULL);
                    break;
                }
                case IDTB_BTN_NEXT:{
                    PyObject_Call(pFuncs[3], PyTuple_New(0), NULL);
                    break;
                }
            }
            PyGILState_Release(d_gstate);
            break;
        }
    }
    //Default tk wndproc
    return CallWindowProc(wndproc_tk, hWnd, message, wParam, lParam);
}

//==================================================

static PyObject* create(PyObject* self, PyObject* args){

    if (!PyArg_ParseTuple(args, "iO!O!O!O!",
        &hWnd,
        &PyFunction_Type, &pFuncs[0],
        &PyFunction_Type, &pFuncs[1],
        &PyFunction_Type, &pFuncs[2],
        &PyFunction_Type, &pFuncs[3]))
    {

        PyErr_SetString(PyExc_TypeError, " wrong arguments :(");
        Py_RETURN_NONE;
    }

    //https://stackoverflow.com/questions/51771072/gwl-wndproc-undeclared
    #ifdef _WIN64
        wndproc_tk = (WNDPROC)GetWindowLongPtr(hWnd, GWLP_WNDPROC);
        CreateThumbnailToolbar(hWnd);
        SetWindowLongPtr(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
    #else
        wndproc_tk = (WNDPROC)GetWindowLong(hWnd, GWL_WNDPROC);
        CreateThumbnailToolbar(hWnd);
        SetWindowLong(hWnd, GWL_WNDPROC, (LONG)WndProc);
    #endif

    Py_RETURN_NONE;
}

static PyObject* update(PyObject* self, PyObject* args){

    if (!PyArg_ParseTuple(args, "i",
        &is_song_playing))
    {
        PyErr_SetString(PyExc_TypeError, " wrong arguments :(");
        Py_RETURN_NONE;
    }

    UpdateThumbnailToolbar(is_song_playing);

    Py_RETURN_NONE;
}

static PyObject* release(PyObject* self, PyObject* args){

    ReleaseThumbnailToolbar();

    Py_RETURN_NONE;
}

static PyMethodDef module_methods[] = {
    {"create", create, METH_VARARGS, "Create ThumbnailToolbar"},
    {"update", update, METH_VARARGS, "Update ThumbnailToolbar"},
    {"release", release, METH_VARARGS, "Release ThumbnailToolbar"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef struct_module = {
    PyModuleDef_HEAD_INIT,
    "ThumbnailToolbar",
    "ThumbnailToolbar like windows media player",
    -1,
    module_methods
};

#ifdef _WIN64
    PyMODINIT_FUNC PyInit_ThumbBar_x64(void) {
        return PyModule_Create(&struct_module);
    }
#else
    PyMODINIT_FUNC PyInit_ThumbBar_x86(void) {
        return PyModule_Create(&struct_module);
    }
#endif