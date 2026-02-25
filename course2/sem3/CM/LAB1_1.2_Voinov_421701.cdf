(* Content-type: application/vnd.wolfram.cdf.text *)

(*** Wolfram CDF File ***)
(* http://www.wolfram.com/cdf *)

(* CreatedBy='Wolfram 14.2' *)

(***************************************************************************)
(*                                                                         *)
(*                                                                         *)
(*  Under the Wolfram FreeCDF terms of use, this file and its content are  *)
(*  bound by the Creative Commons BY-SA Attribution-ShareAlike license.    *)
(*                                                                         *)
(*        For additional information concerning CDF licensing, see:        *)
(*                                                                         *)
(*         www.wolfram.com/cdf/adopting-cdf/licensing-options.html         *)
(*                                                                         *)
(*                                                                         *)
(***************************************************************************)

(*CacheID: 234*)
(* Internal cache information:
NotebookFileLineBreakTest
NotebookFileLineBreakTest
NotebookDataPosition[      1084,         20]
NotebookDataLength[     33997,        923]
NotebookOptionsPosition[     31276,        859]
NotebookOutlinePosition[     31704,        876]
CellTagsIndexPosition[     31661,        873]
WindowFrame->Normal*)

(* Beginning of Notebook Content *)
Notebook[{

Cell[CellGroupData[{
Cell["\:0417\:0430\:0434\:0430\:043d\:0438\:0435 \:21161.2", "Title",
 CellChangeTimes->{{3.905913174082382*^9, 3.905913178388834*^9}, {
  3.9059132261543503`*^9, 3.9059132854099646`*^9}, {3.905913372608173*^9, 
  3.905913372702746*^9}},ExpressionUUID->"cc04d0d6-88db-4bcd-be84-\
01344311c475"],

Cell["", "Subtitle",
 CellChangeTimes->{{3.9059132903534813`*^9, 3.9059133266764593`*^9}, {
  3.969553955585856*^9, 
  3.9695539609230843`*^9}},ExpressionUUID->"1d9ed534-5599-49c4-bbc1-\
03eb1bfd15ee"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:041e\:043f\:0440\:0435\:0434\:0435\:043b\:0438\:043c", " ", 
    "\:043c\:0430\:0442\:0440\:0438\:0446\:0443", " ", "\:0410"}], "*)"}], 
  "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{"k", "=", "9"}], ";"}], "\[IndentingNewLine]", 
   RowBox[{
    RowBox[{
     RowBox[{"a", "[", 
      RowBox[{"i_", ",", " ", "j_"}], "]"}], " ", ":=", " ", 
     FractionBox["1", 
      RowBox[{"i", "+", "j", "-", "1"}]]}], ";", " ", 
    RowBox[{"A", "=", 
     RowBox[{"Table", "[", 
      RowBox[{
       RowBox[{"a", "[", 
        RowBox[{"i", ",", " ", "j"}], "]"}], ",", " ", 
       RowBox[{"{", 
        RowBox[{"i", ",", "1", ",", "7", ",", "1"}], "}"}], ",", 
       RowBox[{"{", 
        RowBox[{"j", ",", "1", ",", "7", ",", "1"}], "}"}]}], "]"}]}], ";"}], 
   "\[IndentingNewLine]", 
   RowBox[{"A", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048146683428993`*^9, 3.904814670707016*^9}, {
   3.9048150739574337`*^9, 3.9048152026645985`*^9}, {3.904815254997858*^9, 
   3.9048152957376604`*^9}, {3.9048153269815025`*^9, 3.904815358770699*^9}, {
   3.904815550889892*^9, 3.9048155524849997`*^9}, {3.904815642531085*^9, 
   3.904815656624695*^9}, 3.9048157042030287`*^9, {3.9048157377649603`*^9, 
   3.9048157984669313`*^9}, {3.9048159093655815`*^9, 3.904815993842948*^9}, {
   3.9048162807952433`*^9, 3.904816335832986*^9}, 3.904817557064978*^9, {
   3.904819647844506*^9, 3.90481965485476*^9}, {3.9048222183743753`*^9, 
   3.9048222324845037`*^9}, {3.972006479626034*^9, 3.972006493384115*^9}},
 CellLabel->"In[1]:=",ExpressionUUID->"436f2075-44db-4973-97ba-a0b70f22ee5f"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {"1", 
      FractionBox["1", "2"], 
      FractionBox["1", "3"], 
      FractionBox["1", "4"], 
      FractionBox["1", "5"], 
      FractionBox["1", "6"], 
      FractionBox["1", "7"]},
     {
      FractionBox["1", "2"], 
      FractionBox["1", "3"], 
      FractionBox["1", "4"], 
      FractionBox["1", "5"], 
      FractionBox["1", "6"], 
      FractionBox["1", "7"], 
      FractionBox["1", "8"]},
     {
      FractionBox["1", "3"], 
      FractionBox["1", "4"], 
      FractionBox["1", "5"], 
      FractionBox["1", "6"], 
      FractionBox["1", "7"], 
      FractionBox["1", "8"], 
      FractionBox["1", "9"]},
     {
      FractionBox["1", "4"], 
      FractionBox["1", "5"], 
      FractionBox["1", "6"], 
      FractionBox["1", "7"], 
      FractionBox["1", "8"], 
      FractionBox["1", "9"], 
      FractionBox["1", "10"]},
     {
      FractionBox["1", "5"], 
      FractionBox["1", "6"], 
      FractionBox["1", "7"], 
      FractionBox["1", "8"], 
      FractionBox["1", "9"], 
      FractionBox["1", "10"], 
      FractionBox["1", "11"]},
     {
      FractionBox["1", "6"], 
      FractionBox["1", "7"], 
      FractionBox["1", "8"], 
      FractionBox["1", "9"], 
      FractionBox["1", "10"], 
      FractionBox["1", "11"], 
      FractionBox["1", "12"]},
     {
      FractionBox["1", "7"], 
      FractionBox["1", "8"], 
      FractionBox["1", "9"], 
      FractionBox["1", "10"], 
      FractionBox["1", "11"], 
      FractionBox["1", "12"], 
      FractionBox["1", "13"]}
    },
    GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
    GridBoxSpacings->{"Columns" -> {
        Offset[0.27999999999999997`], {
         Offset[0.7]}, 
        Offset[0.27999999999999997`]}, "Rows" -> {
        Offset[0.2], {
         Offset[0.4]}, 
        Offset[0.2]}}], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{3.9048159951708508`*^9, 3.904816340685983*^9, 
  3.9048175578046985`*^9, 3.9048196557945356`*^9, 3.9048222740626626`*^9, 
  3.9069644794448433`*^9, 3.9069651418305583`*^9, 3.9069652932426434`*^9, 
  3.972006620753439*^9},
 CellLabel->
  "Out[3]//MatrixForm=",ExpressionUUID->"2f182d11-7270-274a-a02d-\
d34d388e9ba3"]
}, Open  ]],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
    RowBox[{
    "\:041e\:043f\:0440\:0435\:0434\:0435\:043b\:0438\:043c", " ", 
     "\:0432\:0435\:043a\:0442\:043e\:0440"}], "-", 
    RowBox[{"\:0441\:0442\:043e\:043b\:0431\:0435\:0446", " ", "b"}]}], 
   "*)"}], "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{
     RowBox[{"b", "[", "i_", "]"}], ":=", 
     RowBox[{
      RowBox[{"3", "i"}], "-", 
      RowBox[{"2", "k"}]}]}], ";"}], "\[IndentingNewLine]", 
   RowBox[{
    RowBox[{"B", "=", 
     RowBox[{"Table", "[", 
      RowBox[{
       RowBox[{"b", "[", "i", "]"}], ",", 
       RowBox[{"{", 
        RowBox[{"i", ",", "1", ",", "7", ",", "1"}], "}"}]}], "]"}]}], ";"}], 
   "\[IndentingNewLine]", 
   RowBox[{"B", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.904816378140554*^9, 3.9048165966248217`*^9}, 
   3.9048175653550253`*^9, {3.9048196602147045`*^9, 3.904819668044608*^9}, {
   3.9048222411545744`*^9, 3.9048222544970646`*^9}, {3.9720064988671646`*^9, 
   3.9720064995410385`*^9}},
 CellLabel->"In[4]:=",ExpressionUUID->"52f22b8e-8c78-4441-bb23-de208cea72de"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {
       RowBox[{"-", "15"}]},
      {
       RowBox[{"-", "12"}]},
      {
       RowBox[{"-", "9"}]},
      {
       RowBox[{"-", "6"}]},
      {
       RowBox[{"-", "3"}]},
      {"0"},
      {"3"}
     },
     GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
     GridBoxSpacings->{"Columns" -> {
         Offset[0.27999999999999997`], {
          Offset[0.5599999999999999]}, 
         Offset[0.27999999999999997`]}, "Rows" -> {
         Offset[0.2], {
          Offset[0.4]}, 
         Offset[0.2]}}],
    Column], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{
  3.9048165974483757`*^9, 3.90481756606498*^9, 3.9048196688973136`*^9, {
   3.9048222648949385`*^9, 3.90482227411117*^9}, 3.9069644794983315`*^9, 
   3.9069651418683987`*^9, 3.9069652933031754`*^9, 3.9720066213796234`*^9},
 CellLabel->
  "Out[6]//MatrixForm=",ExpressionUUID->"d33fd210-dfb2-9f4a-bdae-\
c16debcac96f"]
}, Open  ]],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
    RowBox[{
    "\:041e\:043f\:0440\:0435\:0434\:0435\:043b\:0438\:043c", " ", 
     "\:0432\:0435\:043a\:0442\:043e\:0440"}], "-", 
    RowBox[{"\:0441\:0442\:043e\:043b\:0431\:0435\:0446", " ", "X"}]}], 
   "*)"}], "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{"X", " ", "=", 
     RowBox[{"{", 
      RowBox[{
       RowBox[{"{", "x1", "}"}], ",", 
       RowBox[{"{", "x2", "}"}], ",", 
       RowBox[{"{", "x3", "}"}], ",", 
       RowBox[{"{", "x4", "}"}], ",", 
       RowBox[{"{", "x5", "}"}], ",", 
       RowBox[{"{", "x6", "}"}], ",", 
       RowBox[{"{", "x7", "}"}]}], "}"}]}], ";"}], "\[IndentingNewLine]", 
   RowBox[{"X", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048166518947163`*^9, 3.90481668909982*^9}, {
   3.9048168103352227`*^9, 3.904816852655043*^9}, {3.9048169220916004`*^9, 
   3.9048169246683865`*^9}, 3.904817348775031*^9, {3.9048175697549005`*^9, 
   3.904817577824885*^9}, {3.904819677955688*^9, 3.9048196824525223`*^9}},
 CellLabel->"In[7]:=",ExpressionUUID->"6a70395b-8962-483c-bbef-8afe1b33d867"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {"x1"},
     {"x2"},
     {"x3"},
     {"x4"},
     {"x5"},
     {"x6"},
     {"x7"}
    },
    GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
    GridBoxSpacings->{"Columns" -> {
        Offset[0.27999999999999997`], {
         Offset[0.7]}, 
        Offset[0.27999999999999997`]}, "Rows" -> {
        Offset[0.2], {
         Offset[0.4]}, 
        Offset[0.2]}}], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{3.9069644794983315`*^9, 3.90696514188409*^9, 
  3.9069652933031754`*^9, 3.97200662140884*^9},
 CellLabel->
  "Out[8]//MatrixForm=",ExpressionUUID->"0f03d294-b181-5b46-ade2-\
2cda649239cc"]
}, Open  ]],

Cell[CellGroupData[{

Cell["\:0430) \:043d\:0430\:0439\:0442\:0438 \:0447\:0438\:0441\:043b\:043e \
\:043e\:0431\:0443\:0441\:043b\:043e\:0432\:043b\:0435\:043d\:043d\:043e\:0441\
\:0442\:0438 \:043c\:0430\:0442\:0440\:0438\:0446\:044b A \:0432 \:043d\:043e\
\:0440\:043c\:0435-\:043c\:0430\:043a\:0441\:0438\:043c\:0443\:043c", \
"Subsection",
 CellChangeTimes->{
  3.906964440125074*^9},ExpressionUUID->"46fb74db-c8ab-40e8-b35c-\
0c9a6d8ce921"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
    RowBox[{
    "\:0412\:044b\:0447\:0438\:0441\:043b\:0438\:043c", " ", 
     "\:0447\:0438\:0441\:043b\:043e", " ", 
     "\:043e\:0431\:0443\:0441\:043b\:043e\:0432\:043b\:0435\:043d\:043d\:043e\
\:0441\:0442\:0438", " ", "\:043f\:043e", " ", 
     "\:043d\:043e\:0440\:043c\:0435"}], "-", 
    "\:043c\:0430\:043a\:0441\:0438\:043c\:0443\:043c"}], "*)"}], 
  "\[IndentingNewLine]", 
  RowBox[{"condA", "=", 
   RowBox[{
    RowBox[{
     RowBox[{"Norm", "[", 
      RowBox[{"A", ",", " ", "Infinity"}], "]"}], "*", 
     RowBox[{"Norm", "[", 
      RowBox[{
       RowBox[{"A", "//", "Inverse"}], ",", " ", "Infinity"}], "]"}]}], " ", "//",
     " ", "N"}]}]}]], "Input",
 CellChangeTimes->{{3.9048183265365763`*^9, 3.904818338994668*^9}, {
  3.904818378554734*^9, 3.904818383554745*^9}, {3.9048184337587233`*^9, 
  3.9048184721048126`*^9}, {3.904818663374809*^9, 3.904818786542117*^9}, {
  3.9048188334985685`*^9, 3.9048188690425053`*^9}, {3.904818948242304*^9, 
  3.9048190613071136`*^9}, {3.9048219109444427`*^9, 3.9048219194943886`*^9}, {
  3.9048219524542637`*^9, 3.9048219528013296`*^9}, {3.906964465481597*^9, 
  3.9069645238209267`*^9}},
 CellLabel->"In[9]:=",ExpressionUUID->"502a9aee-e08b-47df-94a8-64c5877856b2"],

Cell[BoxData["9.851948865`*^8"], "Output",
 CellChangeTimes->{3.9069645245746746`*^9, 3.90696514188409*^9, 
  3.9069652933742657`*^9, 3.9720066214699364`*^9},
 CellLabel->"Out[9]=",ExpressionUUID->"dc1f5780-89da-7947-a10c-e4632eaf3db4"]
}, Open  ]]
}, Open  ]],

Cell[CellGroupData[{

Cell["\:0431) \:0440\:0435\:0448\:0438\:0442\:044c \:0442\:043e\:0447\:043d\
\:0443\:044e \:0441\:0438\:0441\:0442\:0435\:043c\:0443 \:043b\:0438\:043d\
\:0435\:0439\:043d\:044b\:0445 \:0443\:0440\:0430\:0432\:043d\:0435\:043d\
\:0438\:0439", "Subsection",
 CellChangeTimes->{{3.906964572476795*^9, 
  3.9069645746980352`*^9}},ExpressionUUID->"1ece259b-3ad0-4f5a-ac79-\
8da15c154061"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:0420\:0435\:0448\:0438\:043c", " ", 
    "\:0441\:0438\:0441\:0442\:0435\:043c\:0443"}], "*)"}], 
  "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{"sol", " ", "=", " ", 
     RowBox[{"Solve", "[", 
      RowBox[{
       RowBox[{
        RowBox[{"A", ".", "X"}], "==", "B"}], ",", " ", 
       RowBox[{"{", 
        RowBox[{
        "x1", ",", "x2", ",", "x3", ",", "x4", ",", "x5", ",", "x6", ",", 
         "x7"}], "}"}]}], "]"}]}], ";"}], "\[IndentingNewLine]", 
   RowBox[{"sol", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.904816867564739*^9, 3.9048168704551897`*^9}, {
  3.9048169406178355`*^9, 3.9048170651788974`*^9}, {3.904817105985165*^9, 
  3.904817109184884*^9}, {3.904817154455039*^9, 3.9048171739449935`*^9}, {
  3.9048172532751713`*^9, 3.904817443629691*^9}, {3.904817587969761*^9, 
  3.904817656408844*^9}, {3.904819691272646*^9, 3.904819698109322*^9}},
 CellLabel->"In[10]:=",ExpressionUUID->"b2e48c05-1c73-436f-9560-ed778b36ad97"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {
      RowBox[{"x1", "\[Rule]", "903"}], 
      RowBox[{"x2", "\[Rule]", 
       RowBox[{"-", "42336"}]}], 
      RowBox[{"x3", "\[Rule]", "464940"}], 
      RowBox[{"x4", "\[Rule]", 
       RowBox[{"-", "2016000"}]}], 
      RowBox[{"x5", "\[Rule]", "4054050"}], 
      RowBox[{"x6", "\[Rule]", 
       RowBox[{"-", "3792096"}]}], 
      RowBox[{"x7", "\[Rule]", "1333332"}]}
    },
    GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
    GridBoxSpacings->{"Columns" -> {
        Offset[0.27999999999999997`], {
         Offset[0.7]}, 
        Offset[0.27999999999999997`]}, "Rows" -> {
        Offset[0.2], {
         Offset[0.4]}, 
        Offset[0.2]}}], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{
  3.9048172908150845`*^9, 3.904817429895508*^9, {3.9048176138113184`*^9, 
   3.9048176583010073`*^9}, 3.904819698456853*^9, 3.904822274144497*^9, 
   3.906964479545208*^9, 3.9069651418996515`*^9, 3.9069652934055166`*^9, 
   3.9720066215314713`*^9},
 CellLabel->
  "Out[11]//MatrixForm=",ExpressionUUID->"15736492-0cfb-1e4b-a97f-\
0be5be0e9052"]
}, Open  ]],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:041f\:043e\:0434\:0441\:0442\:0430\:0432\:0438\:043c", " ", 
    "\:0437\:043d\:0430\:0447\:0438\:043d\:0438\:044f"}], "*)"}], 
  "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{"sol1", " ", "=", " ", 
     RowBox[{"X", "/.", 
      RowBox[{"Flatten", "[", "sol", "]"}]}]}], ";"}], "\[IndentingNewLine]", 
   RowBox[{"sol1", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.904817694954793*^9, 3.9048177021849732`*^9}, {
  3.904817793274664*^9, 3.904817953894594*^9}, {3.9048197053713355`*^9, 
  3.904819718999487*^9}},
 CellLabel->"In[12]:=",ExpressionUUID->"4e91ca84-e563-4bd3-adc8-226c619e518e"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {"903"},
     {
      RowBox[{"-", "42336"}]},
     {"464940"},
     {
      RowBox[{"-", "2016000"}]},
     {"4054050"},
     {
      RowBox[{"-", "3792096"}]},
     {"1333332"}
    },
    GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
    GridBoxSpacings->{"Columns" -> {
        Offset[0.27999999999999997`], {
         Offset[0.7]}, 
        Offset[0.27999999999999997`]}, "Rows" -> {
        Offset[0.2], {
         Offset[0.4]}, 
        Offset[0.2]}}], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{
  3.9048179249950542`*^9, {3.9048197128522396`*^9, 3.9048197197904625`*^9}, 
   3.9048222741624875`*^9, 3.9069651418996515`*^9, 3.90696529342114*^9, 
   3.972006621550665*^9},
 CellLabel->
  "Out[13]//MatrixForm=",ExpressionUUID->"d98fb673-7569-d143-9d4b-\
2aa0c1d38a56"]
}, Open  ]]
}, Open  ]],

Cell[CellGroupData[{

Cell["\<\
\:0432) \:0440\:0435\:0448\:0438\:0442\:044c \:0442\:0440\:0438 \:0432\:043e\
\:0437\:043c\:0443\:0449\:0435\:043d\:043d\:044b\:0435 \:0441\:0438\:0441\
\:0442\:0435\:043c\:044b, \:0443\:0432\:0435\:043b\:0438\:0447\:0438\:0432 \
\:0437\:043d\:0430\:0447\:0435\:043d\:0438\:0435
\:043f\:0440\:0430\:0432\:043e\:0439 \:0447\:0430\:0441\:0442\:0438 \:0442\
\:043e\:043b\:044c\:043a\:043e \:043f\:043e\:0441\:043b\:0435\:0434\:043d\
\:0435\:0433\:043e \:0443\:0440\:0430\:0432\:043d\:0435\:043d\:0438\:044f \
\:0441\:0438\:0441\:0442\:0435\:043c\:044b \:043f\:043e\:0441\:043b\:0435\
\:0434\:043e\:0432\:0430\:0442\:0435\:043b\:044c\:043d\:043e
\:043d\:0430 0,01%; 0,1% \:0438 \:043d\:0430 1%;\
\>", "Subsection",
 CellChangeTimes->{
  3.906964592386768*^9},ExpressionUUID->"5a8cc687-d9df-4bbd-ae1a-\
b84ac312c6cb"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:0417\:0430\:0434\:0430\:0434\:0438\:043c", " ", 
    "\:0444\:0443\:043d\:043a\:0446\:0438\:044e", " ", 
    "\:0432\:043e\:0437\:043c\:0443\:0449\:0435\:043d\:0438\:044f"}], "*)"}], 
  "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{"\[CapitalDelta]B", "[", "p_", "]"}], " ", "=", " ", 
   RowBox[{"{", 
    RowBox[{"0", ",", "0", ",", "0", ",", "0", ",", "0", ",", "0", ",", 
     RowBox[{
      RowBox[{"B", "[", 
       RowBox[{"[", "7", "]"}], "]"}], "*", 
      SuperscriptBox["0.1", "p"]}]}], "}"}]}]}]], "Input",
 CellChangeTimes->{{3.904820172338109*^9, 3.90482029249584*^9}},
 CellLabel->"In[14]:=",ExpressionUUID->"506d76d3-db38-48a1-ab47-0179b661d142"],

Cell[BoxData[
 RowBox[{"{", 
  RowBox[{"0", ",", "0", ",", "0", ",", "0", ",", "0", ",", "0", ",", 
   RowBox[{"3", " ", 
    SuperscriptBox["0.1`", "p"]}]}], "}"}]], "Output",
 CellChangeTimes->{3.904820298741186*^9, 3.9048222741704946`*^9, 
  3.9069651418996515`*^9, 3.90696529342114*^9, 3.972006621580065*^9},
 CellLabel->"Out[14]=",ExpressionUUID->"fbc10cdc-a660-6046-ac8f-034aaf834fd4"]
}, Open  ]],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:0420\:0435\:0448\:0438\:043c", " ", 
    "\:0432\:043e\:0437\:043c\:0443\:0449\:0435\:043d\:043d\:0443\:044e", " ",
     "\:0441\:0438\:0441\:0442\:0435\:043c\:0443"}], "*)"}], 
  "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{"sol2", "=", 
    RowBox[{"Table", "[", 
     RowBox[{
      RowBox[{"LinearSolve", "[", 
       RowBox[{"A", ",", 
        RowBox[{"B", "+", 
         RowBox[{"\[CapitalDelta]B", "[", "p", "]"}]}]}], "]"}], ",", " ", 
      RowBox[{"{", 
       RowBox[{"p", ",", "2", ",", "4", ",", "1"}], "}"}]}], "]"}]}], ";", 
   RowBox[{"sol2", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048180310098524`*^9, 3.9048181209646854`*^9}, {
  3.904818181597806*^9, 3.9048181851045647`*^9}, {3.904819245408598*^9, 
  3.904819261645039*^9}, {3.9048193001486254`*^9, 3.9048193843444705`*^9}, {
  3.9048194205922427`*^9, 3.9048194742585382`*^9}, {3.9048195349187307`*^9, 
  3.9048195424944725`*^9}, {3.9048195793619175`*^9, 3.9048195828596935`*^9}, {
  3.9048196255885334`*^9, 3.904819641593354*^9}, {3.9048202865663605`*^9, 
  3.9048203136384897`*^9}},
 CellLabel->"In[15]:=",ExpressionUUID->"6f88688d-d5c2-43ec-b520-2ef0bb05675a"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {"1263.3600062718288`", 
      RowBox[{"-", "57471.120249432446`"}], "616291.202394883`", 
      RowBox[{"-", "2.62140480928276`*^6"}], "5.18918401697418`*^6", 
      RowBox[{"-", "4.791013934634832`*^6"}], "1.6663046447959987`*^6"},
     {"939.0360050399577`", 
      RowBox[{"-", "43849.51220039772`"}], "480075.12192384637`", 
      RowBox[{"-", "2.07654048745631`*^6"}], "4.16756341363342`*^6", 
      RowBox[{"-", "3.891987803753812`*^6"}], "1.366629267851672`*^6"},
     {"906.6036049166833`", 
      RowBox[{"-", "42487.351395492435`"}], "466453.51387673325`", 
      RowBox[{"-", "2.0220540552736346`*^6"}], "4.065401353299288`*^6", 
      RowBox[{"-", "3.8020851906656604`*^6"}], "1.3366617301572228`*^6"}
    },
    GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
    GridBoxSpacings->{"Columns" -> {
        Offset[0.27999999999999997`], {
         Offset[0.7]}, 
        Offset[0.27999999999999997`]}, "Rows" -> {
        Offset[0.2], {
         Offset[0.4]}, 
        Offset[0.2]}}], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{{3.9048180914846106`*^9, 3.9048181229644527`*^9}, {
   3.904819467836911*^9, 3.904819475162039*^9}, 3.904819547724468*^9, 
   3.9048195845711718`*^9, 3.904819642151925*^9, 3.904820317796647*^9, 
   3.904822274174492*^9, 3.906965141915334*^9, 3.90696529344328*^9, 
   3.972006621611225*^9},
 CellLabel->
  "Out[15]//MatrixForm=",ExpressionUUID->"c528ad22-24bd-554c-8ae4-\
1e069737386b"]
}, Open  ]]
}, Open  ]],

Cell[CellGroupData[{

Cell["\<\
\:0433) \:043d\:0430\:0439\:0442\:0438 \:043f\:0440\:043e\:0433\:043d\:043e\
\:0437\:0438\:0440\:0443\:0435\:043c\:0443\:044e \:043f\:0440\:0435\:0434\
\:0435\:043b\:044c\:043d\:0443\:044e \:043e\:0442\:043d\:043e\:0441\:0438\
\:0442\:0435\:043b\:044c\:043d\:0443\:044e \:043f\:043e\:0433\:0440\:0435\
\:0448\:043d\:043e\:0441\:0442\:044c \:0440\:0435\:0448\:0435\:043d\:0438\:044f
\:043a\:0430\:0436\:0434\:043e\:0439 \:0432\:043e\:0437\:043c\:0443\:0449\
\:0435\:043d\:043d\:043e\:0439 \:0441\:0438\:0441\:0442\:0435\:043c\:044b\
\>", "Subsection",
 CellChangeTimes->{
  3.9069646159293303`*^9},ExpressionUUID->"1dd4de3f-eec6-496c-b577-\
b140c5e36dc4"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:0412\:044b\:0447\:0438\:0441\:043b\:0438\:043c", " ", 
    "\:0430\:0431\:0441\:043e\:043b\:044e\:0442\:043d\:0443\:044e", " ", 
    "\:043f\:043e\:0433\:0440\:0435\:0448\:043d\:043e\:0441\:0442\:044c"}], 
   "*)"}], "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{"\[CapitalDelta]X", "=", 
     RowBox[{"Table", "[", 
      RowBox[{
       RowBox[{
        RowBox[{"Norm", "[", 
         RowBox[{
          RowBox[{"sol2", "[", 
           RowBox[{"[", "p", "]"}], "]"}], "-", "sol1"}], "]"}], " ", "//", 
        "N"}], ",", " ", 
       RowBox[{"{", 
        RowBox[{"p", ",", "1", ",", "3", ",", "1"}], "}"}]}], "]"}]}], ";"}], 
   "\[IndentingNewLine]", 
   RowBox[{"\[CapitalDelta]X", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048206272944555`*^9, 3.9048206540244427`*^9}, {
  3.9048207902011795`*^9, 3.904821079734313*^9}, {3.9048211689445934`*^9, 
  3.904821263510044*^9}, {3.9048218716423244`*^9, 3.904821874588321*^9}},
 CellLabel->"In[16]:=",ExpressionUUID->"5e673827-b4d3-4e86-b901-8b8527662bcb"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {"1.6693976249242926`*^6"},
      {"166939.77996019917`"},
      {"16693.995463706946`"}
     },
     GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
     GridBoxSpacings->{"Columns" -> {
         Offset[0.27999999999999997`], {
          Offset[0.5599999999999999]}, 
         Offset[0.27999999999999997`]}, "Rows" -> {
         Offset[0.2], {
          Offset[0.4]}, 
         Offset[0.2]}}],
    Column], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{{3.9048211901044445`*^9, 3.9048212647188125`*^9}, 
   3.904821900050268*^9, 3.9048222742160397`*^9, 3.906965141915334*^9, 
   3.90696529344328*^9, 3.9720066216416473`*^9},
 CellLabel->
  "Out[17]//MatrixForm=",ExpressionUUID->"402cd385-9a49-434a-9d90-\
3729be4e1d46"]
}, Open  ]],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:0412\:044b\:0447\:0438\:0441\:043b\:0438\:043c", " ", 
    "\:043f\:0440\:043e\:0433\:043d\:043e\:0437\:0438\:0440\:0443\:0435\:043c\
\:0443\:044e", " ", 
    "\:043f\:0440\:0435\:0434\:0435\:043b\:044c\:043d\:0443\:044e", " ", 
    "\:043e\:0442\:043d\:043e\:0441\:0438\:0442\:0435\:043b\:044c\:043d\:0443\
\:044e", " ", 
    "\:043f\:043e\:0433\:0440\:0435\:0448\:043d\:043e\:0441\:0442\:044c"}], 
   "*)"}], "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{
     SubscriptBox["\[Delta]", "X"], "=", 
     RowBox[{"Table", "[", 
      RowBox[{
       RowBox[{
        RowBox[{"condA", "*", 
         FractionBox[
          RowBox[{"Norm", "[", 
           RowBox[{"\[CapitalDelta]B", "[", "p", "]"}], "]"}], 
          RowBox[{"Norm", "[", 
           RowBox[{"B", "+", 
            RowBox[{"\[CapitalDelta]B", "[", "p", "]"}]}], "]"}]]}], "//", 
        "PercentForm"}], ",", 
       RowBox[{"{", 
        RowBox[{"p", ",", "2", ",", "4", ",", "1"}], "}"}]}], "]"}]}], ";"}], 
   "\[IndentingNewLine]", 
   RowBox[{
    SubscriptBox["\[Delta]", "X"], "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048199004472*^9, 3.9048199285615873`*^9}, 
   3.904819978347228*^9, {3.904820023812504*^9, 3.904820057319338*^9}, {
   3.904820094713258*^9, 3.9048201528425426`*^9}, {3.904820328973796*^9, 
   3.904820499784412*^9}, 3.904820532755375*^9, {3.904820689826395*^9, 
   3.9048207219246655`*^9}, {3.9048213620036554`*^9, 
   3.9048214872892365`*^9}, {3.904821758744486*^9, 3.904821791387273*^9}, {
   3.9048218547341175`*^9, 3.904821892883602*^9}, {3.906965133570387*^9, 
   3.9069651375698953`*^9}, {3.9069652466769896`*^9, 3.9069652978843737`*^9}},
 CellLabel->"In[18]:=",ExpressionUUID->"79c29857-762a-42ff-ab92-a20050f72836"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"131628584%\"\>",
          ShowStringCharacters->False],
         1.3162858393541332`*^6,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"13164985%\"\>",
          ShowStringCharacters->False],
         131649.85240122417`,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"1316520%\"\>",
          ShowStringCharacters->False],
         13165.196934153297`,
         AutoDelete->True],
        PercentForm]}
     },
     GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
     GridBoxSpacings->{"Columns" -> {
         Offset[0.27999999999999997`], {
          Offset[0.5599999999999999]}, 
         Offset[0.27999999999999997`]}, "Rows" -> {
         Offset[0.2], {
          Offset[0.4]}, 
         Offset[0.2]}}],
    Column], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{{3.9048203936827126`*^9, 3.9048204386283774`*^9}, {
   3.9048204741157885`*^9, 3.904820501958144*^9}, 3.9048205337363997`*^9, 
   3.90482145545832*^9, 3.904821489163438*^9, 3.904821862379465*^9, 
   3.904821895657231*^9, 3.9048222742480555`*^9, 3.906965141915334*^9, {
   3.9069652480830135`*^9, 3.906965299591257*^9}, 3.972006621659357*^9},
 CellLabel->
  "Out[19]//MatrixForm=",ExpressionUUID->"73b41b4c-9b0e-6344-b96c-\
1b20de0dda85"]
}, Open  ]]
}, Open  ]],

Cell[CellGroupData[{

Cell["\<\
\:0434) \:043d\:0430\:0439\:0442\:0438 \:043e\:0442\:043d\:043e\:0441\:0438\
\:0442\:0435\:043b\:044c\:043d\:0443\:044e \:043f\:043e\:0433\:0440\:0435\
\:0448\:043d\:043e\:0441\:0442\:044c \:0440\:0435\:0448\:0435\:043d\:0438\
\:044f \:043a\:0430\:0436\:0434\:043e\:0439 \:0432\:043e\:0437\:043c\:0443\
\:0449\:0435\:043d\:043d\:043e\:0439 \:0441\:0438\:0441\:0442\:0435\:043c\
\:044b;
\:0441\:0434\:0435\:043b\:0430\:0442\:044c \:0432\:044b\:0432\:043e\:0434 \
\:043e \:0437\:0430\:0432\:0438\:0441\:0438\:043c\:043e\:0441\:0442\:0438 \
\:043e\:0442\:043d\:043e\:0441\:0438\:0442\:0435\:043b\:044c\:043d\:043e\:0439\
 \:043f\:043e\:0433\:0440\:0435\:0448\:043d\:043e\:0441\:0442\:0438 \:043e\
\:0442 \:0432\:0435\:043b\:0438\:0447\:0438\:043d\:044b
\:0432\:043e\:0437\:043c\:0443\:0449\:0435\:043d\:0438\:044f \:0438 \:0447\
\:0438\:0441\:043b\:0430 \:043e\:0431\:0443\:0441\:043b\:043e\:0432\:043b\
\:0435\:043d\:043d\:043e\:0441\:0442\:0438 \:043c\:0430\:0442\:0440\:0438\
\:0446\:044b A .\
\>", "Subsection",
 CellChangeTimes->{
  3.9069646646818686`*^9},ExpressionUUID->"7e326cd4-3b46-4140-8856-\
855f8ca2c5b6"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{
  RowBox[{"(*", 
   RowBox[{
   "\:0412\:044b\:0447\:0438\:0441\:043b\:0438\:043c", " ", 
    "\:043e\:0442\:043d\:043e\:0441\:0438\:0442\:0435\:043b\:044c\:043d\:0443\
\:044e", " ", 
    "\:043f\:043e\:0433\:0440\:0435\:0448\:043d\:043e\:0441\:0442\:044c"}], 
   "*)"}], "\[IndentingNewLine]", 
  RowBox[{
   RowBox[{
    RowBox[{"\[CurlyEpsilon]", "=", 
     RowBox[{"Table", "[", 
      RowBox[{
       RowBox[{
        FractionBox[
         RowBox[{"\[CapitalDelta]X", "[", 
          RowBox[{"[", "p", "]"}], "]"}], 
         RowBox[{"Norm", "[", 
          RowBox[{"sol2", "[", 
           RowBox[{"[", "p", "]"}], "]"}], "]"}]], "//", "PercentForm"}], ",", 
       RowBox[{"{", 
        RowBox[{"p", ",", "1", ",", "3", ",", "1"}], "}"}]}], "]"}]}], ";"}], 
   "\[IndentingNewLine]", 
   RowBox[{"\[CurlyEpsilon]", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048213124423733`*^9, 3.9048213202537007`*^9}, {
  3.904821546757318*^9, 3.9048215497083225`*^9}, {3.9048216167388573`*^9, 
  3.9048216320534625`*^9}, {3.9048216665542483`*^9, 3.9048217347451043`*^9}, {
  3.906965028569021*^9, 3.9069650329866567`*^9}},
 CellLabel->"In[20]:=",ExpressionUUID->"99b7ef42-646e-4045-9d10-b0d15279f6bb"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"21.57%\"\>",
          ShowStringCharacters->False],
         0.2156749093431592,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"2.676%\"\>",
          ShowStringCharacters->False],
         0.026756384043486448`,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"0.2742%\"\>",
          ShowStringCharacters->False],
         0.002741584286012518,
         AutoDelete->True],
        PercentForm]}
     },
     GridBoxAlignment->{"Columns" -> {{Center}}, "Rows" -> {{Baseline}}},
     GridBoxSpacings->{"Columns" -> {
         Offset[0.27999999999999997`], {
          Offset[0.5599999999999999]}, 
         Offset[0.27999999999999997`]}, "Rows" -> {
         Offset[0.2], {
          Offset[0.4]}, 
         Offset[0.2]}}],
    Column], "\[NoBreak]", ")"}],
  Function[BoxForm`e$, 
   MatrixForm[BoxForm`e$]]]], "Output",
 CellChangeTimes->{3.9048217368910217`*^9, 3.9048220144259768`*^9, 
  3.904822274232074*^9, 3.9069650338264327`*^9, 3.9069651419309464`*^9, 
  3.906965293490164*^9, 3.9720066216897106`*^9},
 CellLabel->
  "Out[21]//MatrixForm=",ExpressionUUID->"bdb2ecaf-51f7-e34b-b71d-\
bc0906f18e4e"]
}, Open  ]]
}, Open  ]]
}, Open  ]]
},
WindowSize->{Full, Full},
WindowMargins->{{Automatic, -5}, {-6, Automatic}},
Magnification:>1. Inherited,
FrontEndVersion->"14.3 for Microsoft Windows (64-bit) (July 8, 2025)",
StyleDefinitions->"Default.nb",
ExpressionUUID->"cad30338-3aea-478d-a187-195ad457e414"
]
(* End of Notebook Content *)

(* Internal cache information *)
(*CellTagsOutline
CellTagsIndex->{}
*)
(*CellTagsIndex
CellTagsIndex->{}
*)
(*NotebookFileOutline
Notebook[{
Cell[CellGroupData[{
Cell[1506, 35, 294, 4, 96, "Title",ExpressionUUID->"cc04d0d6-88db-4bcd-be84-01344311c475"],
Cell[1803, 41, 201, 4, 52, "Subtitle",ExpressionUUID->"1d9ed534-5599-49c4-bbc1-03eb1bfd15ee"],
Cell[CellGroupData[{
Cell[2029, 49, 1658, 36, 107, "Input",ExpressionUUID->"436f2075-44db-4973-97ba-a0b70f22ee5f"],
Cell[3690, 87, 2288, 75, 198, "Output",ExpressionUUID->"2f182d11-7270-274a-a02d-d34d388e9ba3"]
}, Open  ]],
Cell[CellGroupData[{
Cell[6015, 167, 1110, 29, 85, "Input",ExpressionUUID->"52f22b8e-8c78-4441-bb23-de208cea72de"],
Cell[7128, 198, 1042, 34, 143, "Output",ExpressionUUID->"d33fd210-dfb2-9f4a-bdae-c16debcac96f"]
}, Open  ]],
Cell[CellGroupData[{
Cell[8207, 237, 1113, 26, 66, "Input",ExpressionUUID->"6a70395b-8962-483c-bbef-8afe1b33d867"],
Cell[9323, 265, 747, 25, 143, "Output",ExpressionUUID->"0f03d294-b181-5b46-ade2-2cda649239cc"]
}, Open  ]],
Cell[CellGroupData[{
Cell[10107, 295, 424, 7, 53, "Subsection",ExpressionUUID->"46fb74db-c8ab-40e8-b35c-0c9a6d8ce921"],
Cell[CellGroupData[{
Cell[10556, 306, 1281, 28, 47, "Input",ExpressionUUID->"502a9aee-e08b-47df-94a8-64c5877856b2"],
Cell[11840, 336, 236, 3, 32, "Output",ExpressionUUID->"dc1f5780-89da-7947-a10c-e4632eaf3db4"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[12125, 345, 384, 6, 53, "Subsection",ExpressionUUID->"1ece259b-3ad0-4f5a-ac79-8da15c154061"],
Cell[CellGroupData[{
Cell[12534, 355, 1032, 24, 66, "Input",ExpressionUUID->"b2e48c05-1c73-436f-9560-ed778b36ad97"],
Cell[13569, 381, 1197, 32, 46, "Output",ExpressionUUID->"15736492-0cfb-1e4b-a97f-0be5be0e9052"]
}, Open  ]],
Cell[CellGroupData[{
Cell[14803, 418, 677, 16, 66, "Input",ExpressionUUID->"4e91ca84-e563-4bd3-adc8-226c619e518e"],
Cell[15483, 436, 925, 30, 143, "Output",ExpressionUUID->"d98fb673-7569-d143-9d4b-2aa0c1d38a56"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[16457, 472, 822, 14, 105, "Subsection",ExpressionUUID->"5a8cc687-d9df-4bbd-ae1a-b84ac312c6cb"],
Cell[CellGroupData[{
Cell[17304, 490, 721, 17, 49, "Input",ExpressionUUID->"506d76d3-db38-48a1-ab47-0179b661d142"],
Cell[18028, 509, 391, 7, 32, "Output",ExpressionUUID->"fbc10cdc-a660-6046-ac8f-034aaf834fd4"]
}, Open  ]],
Cell[CellGroupData[{
Cell[18456, 521, 1213, 26, 47, "Input",ExpressionUUID->"6f88688d-d5c2-43ec-b520-2ef0bb05675a"],
Cell[19672, 549, 1574, 33, 82, "Output",ExpressionUUID->"c528ad22-24bd-554c-8ae4-1e069737386b"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[21295, 588, 664, 11, 79, "Subsection",ExpressionUUID->"1dd4de3f-eec6-496c-b577-b140c5e36dc4"],
Cell[CellGroupData[{
Cell[21984, 603, 1095, 26, 66, "Input",ExpressionUUID->"5e673827-b4d3-4e86-b901-8b8527662bcb"],
Cell[23082, 631, 879, 24, 78, "Output",ExpressionUUID->"402cd385-9a49-434a-9d90-3729be4e1d46"]
}, Open  ]],
Cell[CellGroupData[{
Cell[23998, 660, 1805, 40, 87, "Input",ExpressionUUID->"79c29857-762a-42ff-ab92-a20050f72836"],
Cell[25806, 702, 1586, 47, 76, "Output",ExpressionUUID->"73b41b4c-9b0e-6344-b96c-1b20de0dda85"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[27441, 755, 1126, 19, 105, "Subsection",ExpressionUUID->"7e326cd4-3b46-4140-8856-855f8ca2c5b6"],
Cell[CellGroupData[{
Cell[28592, 778, 1235, 29, 87, "Input",ExpressionUUID->"99b7ef42-646e-4045-9d10-b0d15279f6bb"],
Cell[29830, 809, 1406, 45, 76, "Output",ExpressionUUID->"bdb2ecaf-51f7-e34b-b71d-bc0906f18e4e"]
}, Open  ]]
}, Open  ]]
}, Open  ]]
}
]
*)

(* NotebookSignature Bv0txRpGQd3m6CKwj1I4iupc *)
