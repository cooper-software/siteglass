/* 
 * Uses a slightly modified version of Douglas Crockford's original JSMin 
 * which can be found here: https://github.com/douglascrockford/JSMin
 */

#include <Python.h>
#include <stdlib.h>
#include <math.h>
 
typedef struct
{
    char *data;
    int size;
    int capacity;
    int offset;
} BufferStream;


static BufferStream *stream_new(const char *string, int size)
{
    BufferStream *stream = malloc(sizeof(BufferStream));
    
    if (!stream)
    {
        return NULL;
    }
    
    if (string == NULL)
    {
        stream->size = 0;
        stream->capacity = 32;
        stream->data = malloc(stream->capacity);
        
        if (!stream->data)
        {
            return NULL;
        }
    }
    else
    {
        stream->size = size;
        stream->capacity = pow(2, ceil(log(size)/log(2)));
        stream->data = malloc(stream->capacity);
        
        if (!stream->data)
        {
            return NULL;
        }
        
        memcpy(stream->data, string, size);
    }
    
    stream->offset = 0;
    
    return stream;
}

static void stream_delete(BufferStream *stream)
{
    if (stream != NULL)
    {
        if (stream->data != NULL)
        {
            free(stream->data);
        }
        
        free(stream);
    }
}

static char stream_getc(BufferStream *stream)
{
    if (stream->offset == stream->size)
    {
        return EOF;
    }
    
    return stream->data[stream->offset++];
}

static void stream_putc(char c, BufferStream *stream)
{
    if (stream->size == stream->capacity)
    {
        stream->capacity *= 2;
        char *old_data = stream->data;
        char *new_data = malloc(stream->capacity);
        
        if (!new_data)
        {
            printf("Out of memory.\n");
            exit(1);
        }
        
        memcpy(new_data, old_data, stream->size);
        free(old_data);
        stream->data = new_data;
    }
    
    stream->data[stream->offset++] = c;
    stream->size++;
}

static void stream_get_contents(BufferStream *stream, char **string, int *size)
{
    if (stream->size == 0)
    {
        *string = NULL;
        *size = 0;
        return;
    }
    
    *string = malloc(stream->size);
    
    if (!string)
    {
        printf("Out of memory.\n");
        exit(1);
    }
    
    memcpy(*string, stream->data, stream->size);
    *size = stream->size;
}


static char *err = NULL;
static BufferStream *instream;
static BufferStream *outstream;

static int   theA;
static int   theB;
static int   theLookahead = EOF;
static int   theX = EOF;
static int   theY = EOF;

static void
reset_error()
{
    err = NULL;
}

static void
error(char* s)
{
    err = s;
}

/* isAlphanum -- return true if the character is a letter, digit, underscore,
        dollar sign, or non-ASCII character.
*/

static int
isAlphanum(int c)
{
    return ((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') ||
        (c >= 'A' && c <= 'Z') || c == '_' || c == '$' || c == '\\' ||
        c > 126);
}


/* get -- return the next character from instream. Watch out for lookahead. If
        the character is a control character, translate it to a space or
        linefeed.
*/

static int
get()
{
    int c = theLookahead;
    theLookahead = EOF;
    if (c == EOF) {
        c = stream_getc(instream);
    }
    if (c >= ' ' || c == '\n' || c == EOF) {
        return c;
    }
    if (c == '\r') {
        return '\n';
    }
    return ' ';
}


/* peek -- get the next character without getting it.
*/

static int
peek()
{
    theLookahead = get();
    return theLookahead;
}


/* next -- get the next character, excluding comments. peek() is used to see
        if a '/' is followed by a '/' or '*'.
*/

static int
next()
{
    int c = get();
    if  (c == '/') {
        switch (peek()) {
        case '/':
            for (;;) {
                c = get();
                if (c <= '\n') {
                    break;
                }
            }
            break;
        case '*':
            get();
            while (c != ' ') {
                switch (get()) {
                case '*':
                    if (peek() == '/') {
                        get();
                        c = ' ';
                    }
                    break;
                case EOF:
                    error("Unterminated comment.");
                    return 0;
                }
            }
            break;
        }
    }
    theY = theX;
    theX = c;
    return c;
}


/* action -- do something! What you do is determined by the argument:
        1   Output A. Copy B to A. Get the next B.
        2   Copy B to A. Get the next B. (Delete A).
        3   Get the next B. (Delete B).
   action treats a string as a single character. Wow!
   action recognizes a regular expression if it is preceded by ( or , or =.
*/

static void
action(int d)
{
    switch (d) {
    case 1:
        if (theA != 0)
        {
            stream_putc(theA, outstream);
        }
        if (
            (theY == '\n' || theY == ' ') &&
            (theA == '+' || theA == '-' || theA == '*' || theA == '/') &&
            (theB == '+' || theB == '-' || theB == '*' || theB == '/')
        ) {
            stream_putc(theY, outstream);
        }
    case 2:
        theA = theB;
        if (theA == '\'' || theA == '"' || theA == '`') {
            for (;;) {
                stream_putc(theA, outstream);
                theA = get();
                if (theA == theB) {
                    break;
                }
                if (theA == '\\') {
                    stream_putc(theA, outstream);
                    theA = get();
                }
                if (theA == EOF) {
                    error("Unterminated string literal.");
                    return;
                }
            }
        }
    case 3:
        theB = next();
        if (theB == '/' && (
            theA == '(' || theA == ',' || theA == '=' || theA == ':' ||
            theA == '[' || theA == '!' || theA == '&' || theA == '|' ||
            theA == '?' || theA == '+' || theA == '-' || theA == '~' ||
            theA == '*' || theA == '/' || theA == '{' || theA == '\n'
        )) {
            stream_putc(theA, outstream);
            if (theA == '/' || theA == '*') {
                stream_putc(' ', outstream);
            }
            stream_putc(theB, outstream);
            for (;;) {
                theA = get();
                if (theA == '[') {
                    for (;;) {
                        stream_putc(theA, outstream);
                        theA = get();
                        if (theA == ']') {
                            break;
                        }
                        if (theA == '\\') {
                            stream_putc(theA, outstream);
                            theA = get();
                        }
                        if (theA == EOF) {
                            error("Unterminated set in Regular Expression literal.");
                            return;
                        }
                    }
                } else if (theA == '/') {
                    switch (peek()) {
                    case '/':
                    case '*':
                        error("Unterminated set in Regular Expression literal.");
                        return;
                    }
                    break;
                } else if (theA =='\\') {
                    stream_putc(theA, outstream);
                    theA = get();
                }
                if (theA == EOF) {
                    error("Unterminated Regular Expression literal.");
                    return;
                }
                stream_putc(theA, outstream);
            }
            theB = next();
            if (err != NULL)
            {
                return;
            }
        }
    }
}


/* jsmin -- Copy the input to the output, deleting the characters which are
        insignificant to JavaScript. Comments will be removed. Tabs will be
        replaced with spaces. Carriage returns will be replaced with linefeeds.
        Most spaces and linefeeds will be removed.
*/

static void
jsmin(const char *string, int string_size,
      char **minified_string, int *minified_string_size)
{
    reset_error();
    instream = stream_new(string, string_size);
    outstream = stream_new(NULL, 0);
    
    if (peek() == 0xEF) {
        get();
        get();
        get();
    }
    theA = 0;
    action(3);
    while (theA != EOF) {
        switch (theA) {
        case ' ':
            action(isAlphanum(theB) ? 1 : 2);
            break;
        case '\n':
            switch (theB) {
            case '{':
            case '[':
            case '(':
            case '+':
            case '-':
            case '!':
            case '~':
                action(1);
                break;
            case ' ':
                action(3);
                break;
            default:
                action(isAlphanum(theB) ? 1 : 2);
            }
            break;
        default:
            switch (theB) {
            case ' ':
                action(isAlphanum(theA) ? 1 : 3);
                break;
            case '\n':
                switch (theA) {
                case '}':
                case ']':
                case ')':
                case '+':
                case '-':
                case '"':
                case '\'':
                case '`':
                    action(1);
                    break;
                default:
                    action(isAlphanum(theA) ? 1 : 3);
                }
                break;
            default:
                action(1);
                break;
            }
        }
        
        if (err != NULL)
        {
            stream_delete(instream);
            stream_delete(outstream);
            return;
        }
    }
    
    stream_get_contents(outstream, minified_string, minified_string_size);
    stream_delete(instream);
    stream_delete(outstream);
}

static PyObject *JSMinError;


static PyObject *
jsmin_minify(PyObject *self, PyObject *args)
{
    const char *javascript;
    int javascript_size;
    
    if (!PyArg_ParseTuple(args, "s#", &javascript, &javascript_size))
    {
        return NULL;
    }
    
    if (javascript[javascript_size-1] == '\0')
    {
        javascript_size--;
    }
    
    char *minified_javascript;
    int minified_javascript_size;
    
    jsmin(javascript, javascript_size, &minified_javascript, &minified_javascript_size);
    
    if (err != NULL)
    {
        PyErr_SetString(JSMinError, err);
        return NULL;
    }
    
    if (!minified_javascript)
    {
        Py_RETURN_NONE;
    }
    else
    {
        PyObject *retval = PyString_FromStringAndSize(minified_javascript, minified_javascript_size);
        free(minified_javascript);
        
        return retval;
    }
}


static PyMethodDef JSMinMethods[] = {
    {"minify", jsmin_minify, METH_VARARGS, "Minify some javascript."},
    {NULL, NULL, 0, NULL}
};


PyMODINIT_FUNC
initjsmin(void)
{
    PyObject *m;

    m = Py_InitModule("siteglass.jsmin", JSMinMethods);
    if (m == NULL)
        return;

    JSMinError = PyErr_NewException("siteglass.jsmin.error", NULL, NULL);
    Py_INCREF(JSMinError);
    PyModule_AddObject(m, "error", JSMinError);
}