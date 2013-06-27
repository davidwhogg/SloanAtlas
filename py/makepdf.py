import Image
import matplotlib.pyplot as plt
import os

imgstart = 88

tex = r'''
\documentclass[compress,handout]{beamer}
\usepackage{helvet}
\usepackage{graphicx}
\newcommand{\plot}[1]{\includegraphics[width=0.25\textwidth,trim=2cm 1cm 2cm 1cm, clip=true]{#1}}
\begin{document}'''

page =r'''\begin{frame}[plain]
\plot{img%d-000.png}
\plot{img%d-000.png}
\plot{img%d-000.png}\\
\plot{img%d-000.png}
\plot{img%d-000.png}
\plot{img%d-000.png}
\end{frame}
''' % (imgstart,imgstart+5,imgstart+10,imgstart+15,imgstart+20,imgstart+25) + '\n'
# page2 =r'''\begin{frame}{MODEL}
# \plot{img%d-002.png}
# \plot{img%d-002.png}
# \plot{img%d-002.png}\\
# \plot{img%d-002.png}
# \plot{img%d-002.png}
# \plot{img%d-002.png}
# \end{frame}
# ''' % (imgstart,imgstart+5,imgstart+10,imgstart+15,imgstart+20,imgstart+25) + '\n'
# page3 =r'''\begin{frame}{DATA-MODEL}
# \plot{img%d-004.png}
# \plot{img%d-004.png}
# \plot{img%d-004.png}\\
# \plot{img%d-004.png}
# \plot{img%d-004.png}
# \plot{img%d-004.png}
# \end{frame}
# ''' % (imgstart,imgstart+5,imgstart+10,imgstart+15,imgstart+20,imgstart+25) + '\n'

# page4 =r'''\begin{frame}{CHI}
# \plot{img%d-006.png}
# \plot{img%d-006.png}
# \plot{img%d-006.png}\\
# \plot{img%d-006.png}
# \plot{img%d-006.png}
# \plot{img%d-006.png}
# \end{frame}
# ''' % (imgstart,imgstart+5,imgstart+10,imgstart+15,imgstart+20,imgstart+25) + '\n'

tex+=page
#tex+=page2
#tex+=page3
#tex+=page4
tex+='''\end{document}'''


fn = 'boundbox.tex'
open(fn,'wb').write(tex)
os.system("pdflatex '%s'" % fn)

