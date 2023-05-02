#include "Python.h"
#include "ShObjIdl_core.h"  //ITaskbarList3
#include "strsafe.h"        //StringCchCopy()

#include <iostream>
#include <vector>

//https://learn.microsoft.com/es-es/windows/win32/shell/taskbar-extensions#thumbnail-toolbars
//https://github.com/microsoft/Windows-classic-samples/blob/main/Samples/Win7Samples/winui/shell/appshellintegration/TaskbarThumbnailToolbar/ThumbnailToolbar.cpp

//==================================================

const unsigned THUMBBTN_ID_OFFSET = 90;

struct BTN{
    unsigned id;
    wchar_t* hovertext;
    PyObject* func;
};

HIMAGELIST himl;
HWND hWnd;
WNDPROC wndproc_tk;
ITaskbarList3* pTaskbarList;

std::vector<BTN> btns;
std::vector<THUMBBUTTON> thumbbar_btns;

//==================================================

HIMAGELIST createImageList(wchar_t* imagefile){
    struct BitMap{
        LPCWSTR pbmp;
        int cx;
    };

    BitMap image = {imagefile, 16 };

    return ImageList_LoadImage(
        NULL,
        image.pbmp,
        image.cx,
        0,
        RGB(255,0,255),
        IMAGE_BITMAP,
        LR_CREATEDIBSECTION | LR_LOADFROMFILE
    );
}

THUMBBUTTON createThumbbarBtn(BTN btn){
    THUMBBUTTON thumbbtn;
    thumbbtn.iId = THUMBBTN_ID_OFFSET+btn.id;
    thumbbtn.dwFlags = THBF_ENABLED;
    thumbbtn.iBitmap = btn.id;
    thumbbtn.dwMask = THB_BITMAP | THB_TOOLTIP | THB_FLAGS;
    StringCchCopy(thumbbtn.szTip, ARRAYSIZE(thumbbtn.szTip), btn.hovertext);

    return thumbbtn;
}

void updateThumbbarBtn(THUMBBUTTON& thumbbtn, BTN btn){
    thumbbtn.iBitmap = btn.id;
    StringCchCopy(thumbbtn.szTip, ARRAYSIZE(thumbbtn.szTip), btn.hovertext);
}

//==================================================

HRESULT CreateThumbBar(HWND hWnd, wchar_t* imagefile, std::vector<BTN> btns, int* btnsset, unsigned btnsset_size){
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

    himl = createImageList(imagefile);
    if (!himl){
        pTaskbarList->Release();
        return (HRESULT)-1;
    }

    hr = pTaskbarList->ThumbBarSetImageList(hWnd, himl);
    if (!SUCCEEDED(hr)){
        ImageList_Destroy(himl);
        pTaskbarList->Release();
        return hr;
    }

    for (unsigned i=0; i<btnsset_size; i++)
        thumbbar_btns.push_back(createThumbbarBtn(btns[btnsset[i]]));

    hr = pTaskbarList->ThumbBarAddButtons(hWnd, (UINT)thumbbar_btns.size(), thumbbar_btns.data());

    return hr;
}

HRESULT UpdateThumbBar(int pos, int i){
    updateThumbbarBtn(thumbbar_btns[pos], btns[i]);

    HRESULT hr = pTaskbarList->ThumbBarUpdateButtons(hWnd, (UINT)thumbbar_btns.size(), thumbbar_btns.data());

    return hr;
}

HRESULT ReleaseThumbBar(){
    ImageList_Destroy(himl);
    HRESULT hr = pTaskbarList->Release();

    return hr;
}

//==================================================

//Processes the message sent when a button is clicked
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam){
    switch (message){
        case WM_COMMAND:{
            for (unsigned i=0; i<btns.size(); i++)
                if (THUMBBTN_ID_OFFSET+i == LOWORD(wParam)){
                    PyGILState_STATE gstate = PyGILState_Ensure();
                    PyObject_Call(btns[i].func, PyTuple_New(0), NULL);
                    PyGILState_Release(gstate);
                }
            break;
        }
    }
    //Default tk wndproc
    return CallWindowProc(wndproc_tk, hWnd, message, wParam, lParam);
}

//==================================================

static PyObject* create(PyObject* self, PyObject* args){

    PyObject* pystr;
    PyObject* pybtns;
    PyObject* pybtnsset;

    if (!PyArg_ParseTuple(args, "IUO!O!",
        &hWnd,
        &pystr,
        &PyTuple_Type, &pybtns,
        &PyTuple_Type, &pybtnsset
    ))
    {
        PyErr_SetString(PyExc_TypeError, " wrong arguments :(");
        Py_RETURN_NONE;
    }
    wchar_t* imagefile = PyUnicode_AsWideCharString(pystr, NULL);

    PyObject* pybtns_iterator = PyObject_GetIter(pybtns);
    while (PyObject* pybtn = PyIter_Next(pybtns_iterator)) {
        BTN btn;
        btn.id = (int)btns.size();

        if (!PyArg_ParseTuple(pybtn, "UO!",
            &pystr,
            &PyFunction_Type, &btn.func
        ))
        {
            PyErr_SetString(PyExc_TypeError, " wrong arguments :(");
            Py_RETURN_NONE;
        }
        btn.hovertext = PyUnicode_AsWideCharString(pystr, NULL);

        btns.push_back(btn);
    }

    unsigned btnsset_size = unsigned(PyTuple_Size(pybtnsset));
    int* btnsset = new int[btnsset_size];
    for (unsigned i=0; i<btnsset_size; i++)
        btnsset[i] = PyLong_AsLong(PyTuple_GetItem(pybtnsset, i));

    //CreateThumbBar(hWnd, imagefile, btns, btnsset, btnsset_size);

    //https://stackoverflow.com/questions/51771072/gwl-wndproc-undeclared
    #ifdef _WIN64
        wndproc_tk = (WNDPROC)GetWindowLongPtr(hWnd, (-4));
        CreateThumbBar(hWnd, imagefile, btns, btnsset, btnsset_size);
        SetWindowLongPtr(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
    #else
        wndproc_tk = (WNDPROC)GetWindowLong(hWnd, GWL_WNDPROC);
        CreateThumbBar(hWnd, imagefile, btns, btnsset, btnsset_size);
        SetWindowLong(hWnd, GWL_WNDPROC, (LONG)WndProc);
    #endif

    PyMem_Free(imagefile);
    delete[] btnsset;

    Py_RETURN_NONE;
}

static PyObject* update(PyObject* self, PyObject* args){

    int pos, id;

    if (!PyArg_ParseTuple(args, "ii",
        &pos,
        &id
    ))
    {
        PyErr_SetString(PyExc_TypeError, " wrong arguments :(");
        Py_RETURN_NONE;
    }

    UpdateThumbBar(pos, id);

    Py_RETURN_NONE;
}

static PyObject* release(PyObject* self, PyObject* args){

    ReleaseThumbBar();

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
#define PyInit_ThumbBar PyInit_ThumbBar_x64
#else
#define PyInit_ThumbBar PyInit_ThumbBar_Win32
#endif

PyMODINIT_FUNC PyInit_ThumbBar(void) {
    return PyModule_Create(&struct_module);
}