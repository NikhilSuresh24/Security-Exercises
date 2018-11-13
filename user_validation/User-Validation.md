
# Table of Contents
- [Table of Contents](#table-of-contents)
- [Number.py](#numberpy)
    - [Breaking Number.py](#breaking-numberpy)
    - [Fixing number.py](#fixing-numberpy)
    - [Consequences of Break](#consequences-of-break)
- [Comments.html](#commentshtml)
    - [Breaking Comments.html](#breaking-commentshtml)
    - [Fixing Comments.html](#fixing-commentshtml)
    - [Consequences of Break](#consequences-of-break)
- [buffer_overflow.c](#bufferoverflowc)
    - [Breaking buffer_overflow.c](#breaking-bufferoverflowc)
    - [Fixing buffer_overflow.c](#fixing-bufferoverflowc)
    - [Consequences of Break](#consequences-of-break)

# Number.py

## Breaking Number.py

number.py (Python 2)

    favorite = input('What is your favorite number? ')
    print 'I like the number {}, too!'.format(favorite)

In python 2, the `input` keyword took in user input and executed it with the `eval` keyword. The problem with this is that python code inputted to the program will be run in the `print` statement. To access the contents of files in the directory that `number.py` resides in, I ran:

    [i + " : " + "".join(open(i).readlines()) for i in __import__('os').listdir(".") if __import__('os').path.isfile(i)]

This statement prints the name of every `file` in the current directory and prints the contents of the files. It imports `os` to find all things in the directory and check if each thing is a file (not a directory). The '__import__' keyword must be used because the usually used `import` statement cannot be used with `eval`.

## Fixing number.py

The easiest fix of `number.py` is to use it in python 3, because `input` was patched in python 3 to not evaluate the input it receives. To fix it in python 2, using `raw_input` instead of `input` would prevent input from running.

## Consequences of Break

As stated in [California Legislation](http://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=502.), running the code above would fall under Larceny:

    (2) Knowingly accesses and without permission takes, copies, or makes use of any data from a computer, computer system, or computer network, or takes or copies any supporting documentation, whether existing or residing internal or external to a computer, computer system, or computer network.

If the creator of the program did not give you permission to run this code, you could be charged with Larceny.

# Comments.html

## Breaking Comments.html

Coments.html

    <!doctype html>
    <html>

    <head>
        <meta charset="utf8">
    </head>

    <body>
        <div>
            <label for="commentText">New Comment:</label>
        </div>
        <div>
            <textarea id="commentText" cols="80" rows="10"></textarea>
        </div>

        <div>
            <button type="button" id="addComment">Add Comment</button>
        </div>

        <div id="comments">
            <hr />
        </div>

        <script>
            var highlight = true;
            document.getElementById('addComment').addEventListener(
                'click',
                function () {
                    var commentsElement = document.getElementById('comments');

                    var newDiv = document.createElement('div');

                    if (highlight) {
                        newDiv.setAttribute('style', 'background-color: lightgray');
                    }
                    highlight = !highlight;

                    var dateDiv = document.createElement('div');
                    dateDiv.innerHTML = Date();
                    newDiv.appendChild(dateDiv);

                    var textDiv = document.createElement('div');
                    textDiv.innerHTML = document.getElementById('commentText').value;
                    newDiv.appendChild(textDiv);

                    commentsElement.appendChild(newDiv);
                    commentsElement.appendChild(document.createElement('hr'));
                }
            );
        </script>
    </body>

    </html>

The primary problem with `Comments.html` is the use of the `innerHTML`, which allows javascript to be run. In this case, the contents of the comments box provided are run, if they are code. Even though in HTML5 `<script>` tags cannot be executed through `innerHTML`, we can get around this by using an `img` tag as shown below.

    <img src="x" onerror=alert("Running code through html")>

Although this code only creates an alert, the code run on error could be changed to do something far more malicious. Because the script cannot find an image at the source "x", it errors out, and runs the on error code.

## Fixing Comments.html

Because the purpose of this program is to show the text posted in the comment box, and not run the code in the comment box, switching out the `innerHTML` call for a `textContent` call would simply set the text of the input to part of the output html, and not run code.

## Consequences of Break

The same larceny rule would apply to this example as well. 

# buffer_overflow.c

## Breaking buffer_overflow.c

buffer_overflow.c

    // from http://stackoverflow.com/questions/34247068/buffer-overflow-does-not-work-on-mac-osx-el-capitan
    #include <stdio.h>
    #include <string.h>

    int check_authentication(char *password) {
        int auth_flag = 0;
        char password_buffer[16];

        strcpy(password_buffer, password);

        if (strcmp(password_buffer, "password") == 0) {
            auth_flag = 1;
        }

        return auth_flag;
    }

    int main(int argc, char* argv[]) {
        if (argc < 2) {
            printf("Usage: %s <password>\n", argv[0]);
        }

        if (check_authentication(argv[1])) {
            printf("Access Granted.\n");
        } else {
            printf("Access Denied.\n");
        }
    }

When compiled with the following command:

    gcc -fno-stack-protector -D_FORTIFY_SOURCE=0 buffer_overflow.c

This authentication program can falsely authenticate a password with a buffer overflow. When the compiled program is run with a password of a specific length as shown below, access is granted.

    ./a.out 123456789012345678901

This is because the program only assigns a certain amount of memory space to store the password. Since we compiled the program without a stack protector, there is no check to see if part of the program is overwriting the memory assigned to different parts of code. This password overwrites the memory that points to the `auth_flag`, which bypasses it and provides access. 

## Fixing buffer_overflow.c

Like [number.py](#Fixing-number.py), `buffer_overflow.c` can be fixed in two ways. First, it can be compiled without the `-fno-stack-protector` flag and `-D_FORTIFY_SOURCE=0` flag. This would prevent the stack from being overwritten by functions within itself. 

Additionally, the program `check_authenication` function in `buffer_overflow.c` can be edited to prevent the password buffer from being overflowed. By using `strncopy` instead of `strcopy`, we can specify how large the password buffer should be. The program will then disregard any additional input.

    strncpy(password_buffer, password, 16);

## Consequences of Break

Similar to the other two programs, this would classify as larceny in California. In Alaska, it would classify as a [Class C felony](http://www.akleg.gov/basis/statutes.asp#11.46.740), which can receive sentences between 10 and 40 years and up to an $100,000 fine.



