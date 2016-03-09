
import sys, string, os
import argparse
import subprocess
import StringIO
import contextlib
import difflib
import imp
import traceback

# # Setup our working environment
# repoDir = os.path.dirname(os.path.realpath(__file__))
# extDir = os.path.join(repoDir, 'Ext')

# if 'FABRIC_EXTS_PATH' not in os.environ or os.environ['FABRIC_EXTS_PATH'].find(extDir) == -1:
#     en = os.path.join(repoDir, 'environment.py')
#     imp.load_source('environment', en)

import FabricEngine.Core

failedTests = []
updatedReferences = []
filteredLines = ['Loaded extension', 'Registered extension', 'IRCache', 'Loading DFG presets', '[Event', '[Progress', '[Suspend', '[Resume',]

def emitMessage(arg0, arg1, msg):
    lines = msg.split('\n')
    for line in lines:
        lineLen = len(line)
        if line.startswith('[FABRIC'):
            end = line.find(']')
            line = line[end+2:]
        for l in filteredLines:
            if line.startswith(l):
                return
        line = line.rstrip()
        print line

client = FabricEngine.Core.createClient({ 'reportCallback': emitMessage, 'guarded': True })

operator = client.DG.createOperator('unitTestOp')
operator.setEntryPoint('entry')
operator.setSourceCode('operator entry(){}');
# operator.setMainThreadOnly(True)

binding = client.DG.createBinding()
binding.setOperator(operator)
binding.setParameterLayout([])

dgNode = client.DG.createNode('unitTestNode')
dgNode.bindings.append(binding)


def checkTestOutput(filepath, output, update):
    referencefile = os.path.splitext(filepath)[0] + '.out'
    referencefileExists = os.path.exists(referencefile)
    match = False
    if referencefileExists:
        referenceTxt = str(open( referencefile ).read())
        match = (referenceTxt == output)

    if not referencefileExists or update:
        if not match:
            with open(referencefile, 'w') as f:
                f.write(output)

                if referencefileExists:
                    print "Reference Updated:" + referencefile
                else:
                    print "Reference Created:" + referencefile

            updatedReferences.append(referencefile)

        else:
            print "Reference is Valid:" + referencefile
    else:
        if match:
            print "Test Passed:" + filepath
        else:
            print "Test Failed:" + filepath
            resultfile = os.path.splitext(filepath)[0]+'.result'
            with open(resultfile, 'w') as f:
                f.write(output)

            d = difflib.Differ()
            diff = d.compare(referenceTxt.splitlines(), output.splitlines())
            print '\n'.join(diff)

            failedTests.append(filepath)


def runPytonTest(filepath, update):
    print "Running Python test:" + filepath

    tmp_stdout = sys.stdout

    class stdoutProxy():
        def __init__(self):
            self.output = []

        def write(self, msg):
            tmp_stdout.write(msg)

            lines = msg.split('\n')
            for line in lines:
                lineLen = len(line)
                if lineLen == 0:
                    return
                if line.startswith('[FABRIC'):
                    end = line.find(']')
                    line = line[end+2:]

                for l in filteredLines:
                    if line.startswith(l):
                        return
                line = line.rstrip()
                self.output.append(line)

    sys.stdout = stdoutProxy()

    try:
        execfile( filepath, {} )
    except:
        traceback_lines = traceback.format_exc().split('\n')
        # Remove traceback mentioning this file, and a linebreak
        for i in (3,2,1,-1):
            traceback_lines.pop(i)
        text = '\n'.join(traceback_lines)
        print text

    output = '\n'.join(sys.stdout.output)
    sys.stdout = tmp_stdout

    checkTestOutput(filepath, output, update)


def runKLTest(filepath, update):
    print "Running KL test:" + filepath

    if True:
        cmdstring = "kl.exe " + filepath
        # # Call the kl tool piping output to the output buffer.
        proc = subprocess.Popen(cmdstring, stdout=subprocess.PIPE)

        output = ""
        while True:
            line = proc.stdout.readline()
            if line != '':
                output += line.rstrip() + '\n'
            else:
                break
    else:

        klCode = str(open( filepath ).read())

        def printErrors():
            print 'printErrors'
            errorText = []
            errorText.append('-----------------------------------')
            # construct error information
            diagnostics = operator.getDiagnostics()
            foundError = False
            for diagnostic in operator.getDiagnostics():
                foundError = True
                if 'filename' in diagnostic and os.path.exists(diagnostic['filename']):
                    errorText.append("Error in " + diagnostic['filename'])
                    errorText.append(diagnostic['filename'] + ':' + str(diagnostic['line']) + ':' + str(diagnostic['column']) + ": " + str(diagnostic['level']) + ": " + diagnostic['desc'])
                    klCodeLines = open(diagnostic['filename']).read().split('\n')
                else:
                    errorText.append("Error in " + filepath)
                    errorText.append(str(diagnostic['line']) + ':' + str(diagnostic['column']) + ": " + str(diagnostic['level']) + ": " + diagnostic['desc'])
                    klCodeLines = klCode.split('\n')

            errorLine = diagnostic['line'] - 1
            minLine = int(max(errorLine - 2, 0))
            maxLine = int(min(errorLine + 2, len(klCodeLines)-1))
            for line in range(minLine, maxLine+1):
                codeLine = str(line+1)
                while len(codeLine) < 4:
                        codeLine = '0' + codeLine
                if line == errorLine:
                        codeLine = codeLine + ' > '
                else:
                        codeLine = codeLine + '   '
                codeLine += klCodeLines[line]
                errorText.append(codeLine)
            errorText.append('-----------------------------------')
            if foundError:
                errorText.insert(0, 'Compilation error while compiling test: \''+filepath+'\'')
                print '\n'.join(errorText)



        consoleout = sys.stdout
        class stdoutProxy():
            def __init__(self):
                self.output = ""

            def write(self, text):
                self.output += text
                consoleout.write(text)

        sys.stdout = stdoutProxy()

        try:
            operator.setSourceCode(klCode);
            if len(operator.getErrors()) > 0:
                printErrors()
            else:
                dgNode.evaluate()
            output = sys.stdout.output

        except Exception as e:
            output = sys.stdout.output
            output += str(e)
        sys.stdout = consoleout

    # Now remove all the output that comes from Fabric Engine loading...
    lines = output.split('\n')
    strippedlines = []
    for line in lines:
        lineLen = len(line)
        if line.startswith('[FABRIC'):
            end = line.find(']')
            line = line[end+2:]
        if line.startswith('Loaded extension') or line.startswith('[Event') or line.startswith('[Progress') or line.startswith('[Suspend') or line.startswith('[Resume'):
            continue
        line = line.rstrip()
        strippedlines.append(line)

    output = '\n'.join(strippedlines)

    checkTestOutput(filepath, output, update)



def runTest(filepath, update):
    skipile = os.path.splitext(filepath)[0]+'.skip'
    if os.path.exists(skipile):
        print "Test Skipped:" + filepath
        return

    if filepath.endswith(".py"):
        runPytonTest( filepath, update )
    elif filepath.endswith(".kl"):
        runKLTest( filepath, update )


def run(testsRootDir):
    print "======================================"
    print "Running Tests in " + testsRootDir
    # Parse the commandline args.
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=False, help = "The python or kl File to use in the test (optional)")
    parser.add_argument('--folder', required=False, help = "The root folder to test. (optional)")
    parser.add_argument('--update', required=False, action='store_const', const=True, default=False, help = "Force the update of the reference file(s). (optional)")
    args = parser.parse_args()
    update = args.update

    if args.file is not None:
        if os.path.exists(args.file):
            runTest(args.file, update)
        else:
            filepath = os.path.join(testsRootDir, args.file)
            runTest(filepath, update)
    else:
        if args.folder is not None:
            testsDir = os.path.join(testsRootDir, args.folder)
        else:
            testsDir = testsRootDir
        for root, dirs, files in os.walk(testsDir):
            for folderName in dirs:
                if os.path.exists(os.path.join(root, folderName)+'.skip'):
                    print "Test Folder Skipped:" + folderName
                    dirs.remove(folderName)  # don't visit skipped directories

            # Clean all result files before running tests.
            for filename in files:
                if filename.endswith(".result"):
                    os.remove(os.path.join(root, filename))

            for filename in [name for name in files if name != 'runTests.py']:
                filepath = os.path.join(root, filename)
                runTest(filepath, update)

        if not update:
            if len(failedTests) > 0:
                print "======================================"
                print "FAILED TESTS"

                for filepath in failedTests:
                    print filepath
            else:
                print "======================================"
                print "ALL TESTS PASSED"
        else:
            if len(updatedReferences) > 0:
                print "======================================"
                print "UPDATED TESTS"

                for filepath in updatedReferences:
                    print filepath


if __name__ == '__main__':
    testsRootDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Tests')
    run(testsRootDir)

