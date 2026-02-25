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
NotebookDataLength[     32616,        877]
NotebookOptionsPosition[     29943,        812]
NotebookOutlinePosition[     30550,        834]
CellTagsIndexPosition[     30507,        831]
WindowFrame->Normal*)

(* Beginning of Notebook Content *)
Notebook[{

Cell[CellGroupData[{
Cell["\:0417\:0430\:0434\:0430\:043d\:0438\:0435 \:21161.1", "Title",
 CellChangeTimes->{{3.905913174082382*^9, 3.905913178388834*^9}, {
  3.9059132261543503`*^9, 
  3.9059132854099646`*^9}},ExpressionUUID->"046d3c4c-88d4-47a7-835d-\
2e3a362b76a6"],

Cell["\:0421\:0442\:0443\:0434\:0435\:043d\:0442 \:0433\:0440\:0443\:043f\
\:043f\:044b 421701, \:0412\:043e\:0438\:043d\:043e\:0432 \:0412\:043b\:0430\
\:0434\:0438\:0441\:043b\:0430\:0432", "Subtitle",
 CellChangeTimes->{{3.9059132903534813`*^9, 3.9059133266764593`*^9}, {
  3.969553858457473*^9, 3.969553869153823*^9}, {3.9720068108251534`*^9, 
  3.9720068163390903`*^9}},ExpressionUUID->"78f3ad62-952d-4eb4-809c-\
3b3153d84216"],

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
     RowBox[{"If", "[", 
      RowBox[{
       RowBox[{"i", "==", "j"}], ",", " ", 
       RowBox[{"i", "+", "1"}], ",", " ", 
       RowBox[{"If", "[", 
        RowBox[{
         RowBox[{"i", ">", "j"}], ",", " ", "1", ",", " ", "2", ",", "0"}], 
        "]"}], ",", "0"}], "]"}]}], ";", " ", 
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
   3.904819647844506*^9, 3.90481965485476*^9}, {3.972006820547138*^9, 
   3.972006838221283*^9}},
 CellLabel->"In[64]:=",ExpressionUUID->"436f2075-44db-4973-97ba-a0b70f22ee5f"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {"2", "2", "2", "2", "2", "2", "2"},
     {"1", "3", "2", "2", "2", "2", "2"},
     {"1", "1", "4", "2", "2", "2", "2"},
     {"1", "1", "1", "5", "2", "2", "2"},
     {"1", "1", "1", "1", "6", "2", "2"},
     {"1", "1", "1", "1", "1", "7", "2"},
     {"1", "1", "1", "1", "1", "1", "8"}
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
  3.9048159951708508`*^9, 3.904816340685983*^9, 3.9048175578046985`*^9, 
   3.9048196557945356`*^9, 3.9069636184330153`*^9, 3.906964254009261*^9, {
   3.9069650882779293`*^9, 3.9069651002346883`*^9}, 3.9720069366467495`*^9},
 CellLabel->
  "Out[66]//MatrixForm=",ExpressionUUID->"7d75c1a8-5870-f147-8ab2-\
d36f4b56717d"]
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
      RowBox[{"2", "*", "k", "*", "i"}], "-", 
      SuperscriptBox["i", "2"]}]}], ";"}], "\[IndentingNewLine]", 
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
   3.972006843673271*^9, 3.972006844395708*^9}},
 CellLabel->"In[67]:=",ExpressionUUID->"52f22b8e-8c78-4441-bb23-de208cea72de"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {"17"},
      {"32"},
      {"45"},
      {"56"},
      {"65"},
      {"72"},
      {"77"}
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
  3.9048165974483757`*^9, 3.90481756606498*^9, 3.9048196688973136`*^9, 
   3.906963729622769*^9, 3.906964254058442*^9, {3.9069650883377757`*^9, 
   3.9069651002882214`*^9}, 3.972006936777668*^9},
 CellLabel->
  "Out[69]//MatrixForm=",ExpressionUUID->"563ce523-a946-8c42-af20-\
17046cd99749"]
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
 CellLabel->"In[70]:=",ExpressionUUID->"6a70395b-8962-483c-bbef-8afe1b33d867"],

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
 CellChangeTimes->{
  3.9048168536348066`*^9, 3.904816925617053*^9, {3.9048175702550645`*^9, 
   3.904817580548234*^9}, 3.904819683302402*^9, 3.906964126467535*^9, 
   3.9069642540788946`*^9, {3.9069650883377757`*^9, 3.9069651002882214`*^9}, 
   3.972006936786152*^9},
 CellLabel->
  "Out[71]//MatrixForm=",ExpressionUUID->"6509c465-3054-714a-b122-\
950197a14001"]
}, Open  ]],

Cell[CellGroupData[{

Cell["\:0430) \:043d\:0430\:0439\:0442\:0438 \:0447\:0438\:0441\:043b\:043e \
\:043e\:0431\:0443\:0441\:043b\:043e\:0432\:043b\:0435\:043d\:043d\:043e\:0441\
\:0442\:0438 \:043c\:0430\:0442\:0440\:0438\:0446\:044b A \:0432 \:043d\:043e\
\:0440\:043c\:0435-\:043c\:0430\:043a\:0441\:0438\:043c\:0443\:043c", \
"Subsection",
 CellChangeTimes->{{3.9069635214880056`*^9, 
  3.9069635235067854`*^9}},ExpressionUUID->"6f0e3deb-e73d-46f1-bc84-\
ffc659383b26"],

Cell[CellGroupData[{

Cell[BoxData[
 RowBox[{"condA", "=", 
  RowBox[{
   RowBox[{"Norm", "[", 
    RowBox[{"A", ",", " ", "Infinity"}], "]"}], "*", 
   RowBox[{"Norm", "[", 
    RowBox[{
     RowBox[{"A", "//", "Inverse"}], ",", " ", "Infinity"}], 
    "]"}]}]}]], "Input",
 CellChangeTimes->{{3.9048183265365763`*^9, 3.904818338994668*^9}, {
  3.904818378554734*^9, 3.904818383554745*^9}, {3.9048184337587233`*^9, 
  3.9048184721048126`*^9}, {3.904818663374809*^9, 3.904818786542117*^9}, {
  3.9048188334985685`*^9, 3.9048188690425053`*^9}, {3.904818948242304*^9, 
  3.9048190613071136`*^9}, {3.9048219109444427`*^9, 3.9048219194943886`*^9}, {
  3.9048219524542637`*^9, 3.9048219528013296`*^9}, {3.906963587730547*^9, 
  3.9069635909684725`*^9}},
 CellLabel->"In[72]:=",ExpressionUUID->"502a9aee-e08b-47df-94a8-64c5877856b2"],

Cell[BoxData["25"], "Output",
 CellChangeTimes->{{3.9048189952448483`*^9, 3.9048190255546713`*^9}, 
   3.9048219215643044`*^9, 3.9048219540195274`*^9, 3.906963592255415*^9, 
   3.906963625830762*^9, 3.9069642541005287`*^9, {3.906965088350257*^9, 
   3.9069651002882214`*^9}, 3.9720069368060417`*^9},
 CellLabel->"Out[72]=",ExpressionUUID->"61b7dfbc-368a-104d-82ea-dd9c6efe0386"]
}, Open  ]]
}, Open  ]],

Cell[CellGroupData[{

Cell["\:0431) \:0440\:0435\:0448\:0438\:0442\:044c \:0442\:043e\:0447\:043d\
\:0443\:044e \:0441\:0438\:0441\:0442\:0435\:043c\:0443 \:043b\:0438\:043d\
\:0435\:0439\:043d\:044b\:0445 \:0443\:0440\:0430\:0432\:043d\:0435\:043d\
\:0438\:0439", "Subsection",
 CellChangeTimes->{{3.9069636569058714`*^9, 3.9069636630333676`*^9}, {
  3.906964557631766*^9, 
  3.9069645597907085`*^9}},ExpressionUUID->"a1b0e069-378c-42cd-833d-\
4b70eea3c783"],

Cell[CellGroupData[{

Cell[BoxData[{
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
 RowBox[{"sol", "//", "MatrixForm"}]}], "Input",
 CellChangeTimes->{{3.904816867564739*^9, 3.9048168704551897`*^9}, {
  3.9048169406178355`*^9, 3.9048170651788974`*^9}, {3.904817105985165*^9, 
  3.904817109184884*^9}, {3.904817154455039*^9, 3.9048171739449935`*^9}, {
  3.9048172532751713`*^9, 3.904817443629691*^9}, {3.904817587969761*^9, 
  3.904817656408844*^9}, {3.904819691272646*^9, 3.904819698109322*^9}, {
  3.906963650454173*^9, 3.906963650940193*^9}},
 CellLabel->"In[73]:=",ExpressionUUID->"b2e48c05-1c73-436f-9560-ed778b36ad97"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {
      RowBox[{"x1", "\[Rule]", 
       RowBox[{"-", 
        FractionBox["2781", "140"]}]}], 
      RowBox[{"x2", "\[Rule]", 
       RowBox[{"-", 
        FractionBox["681", "140"]}]}], 
      RowBox[{"x3", "\[Rule]", 
       FractionBox["229", "140"]}], 
      RowBox[{"x4", "\[Rule]", 
       FractionBox["2227", "420"]}], 
      RowBox[{"x5", "\[Rule]", 
       FractionBox["793", "105"]}], 
      RowBox[{"x6", "\[Rule]", 
       FractionBox["188", "21"]}], 
      RowBox[{"x7", "\[Rule]", 
       FractionBox["137", "14"]}]}
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
   3.9048176583010073`*^9}, 3.904819698456853*^9, {3.906964121192944*^9, 
   3.9069641309461136`*^9}, 3.9069642541285224`*^9, {3.9069650883582644`*^9, 
   3.9069651003196316`*^9}, 3.9720069368266144`*^9},
 CellLabel->
  "Out[74]//MatrixForm=",ExpressionUUID->"d4be4226-d95a-9347-a100-\
129c12a7fb02"]
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
 CellLabel->"In[75]:=",ExpressionUUID->"4e91ca84-e563-4bd3-adc8-226c619e518e"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {
      RowBox[{"-", 
       FractionBox["2781", "140"]}]},
     {
      RowBox[{"-", 
       FractionBox["681", "140"]}]},
     {
      FractionBox["229", "140"]},
     {
      FractionBox["2227", "420"]},
     {
      FractionBox["793", "105"]},
     {
      FractionBox["188", "21"]},
     {
      FractionBox["137", "14"]}
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
   3.906964134060995*^9, 3.906964254135522*^9, {3.9069650883628597`*^9, 
   3.9069651003507833`*^9}, 3.9720069368331566`*^9},
 CellLabel->
  "Out[76]//MatrixForm=",ExpressionUUID->"ff715ca6-490b-0548-87e6-\
b2cae049b40d"]
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
 CellChangeTimes->{{3.906963694785554*^9, 
  3.9069637117721543`*^9}},ExpressionUUID->"70ae7b08-6a93-4e42-be19-\
258b30f3a8cd"],

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
   RowBox[{
    RowBox[{
     RowBox[{"\[CapitalDelta]B", "[", "p_", "]"}], " ", "=", " ", 
     RowBox[{"{", 
      RowBox[{"0", ",", "0", ",", "0", ",", "0", ",", "0", ",", "0", ",", 
       RowBox[{
        RowBox[{"B", "[", 
         RowBox[{"[", "7", "]"}], "]"}], "*", 
        SuperscriptBox["0.1", "p"]}]}], "}"}]}], ";"}], "\n", 
   RowBox[{"(*", 
    RowBox[{
     RowBox[{
     "\:0420\:0435\:0448\:0438\:043c", " ", 
      "\:0432\:043e\:0437\:043c\:0443\:0449\:0435\:043d\:043d\:0443\:044e", " ", 
      RowBox[{
      "\:0441\:0438\:0441\:0442\:0435\:043c\:0443", ".", " ", 
       "\:0420\:0435\:0448\:0435\:043d\:0438\:0435"}], " ", 
      "\:0437\:0430\:043f\:0438\:0448\:0435\:043c", " ", "\:0432", " ", 
      "\:0432\:0438\:0434\:0435", " ", 
      "\:043c\:0430\:0442\:0440\:0438\:0446\:044b"}], ",", " ", 
     RowBox[{
      RowBox[{
      "\:0433\:0434\:0435", " ", 
       "\:0441\:0442\:043e\:0440\:043e\:043a\:0430"}], " ", "-", " ", 
      RowBox[{
      "\:0440\:0435\:0448\:0435\:043d\:0438\:0435", " ", 
       "\:0441\:0438\:0441\:0442\:0435\:043c\:044b", " ", "\:0441", " ", 
       "\:043e\:043f\:0440\:0435\:0434\:0435\:043b\:0451\:043d\:043d\:044b\
\:043c", " ", 
       "\:0432\:043e\:0437\:043c\:0443\:0449\:0435\:043d\:0438\:0435\:043c"}]}\
]}], "*)"}], "\[IndentingNewLine]", 
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
    RowBox[{"sol2", "//", "MatrixForm"}]}]}]}]], "Input",
 CellChangeTimes->{{3.904820172338109*^9, 3.90482029249584*^9}, {
  3.906963742347967*^9, 3.9069637442954025`*^9}, {3.9069638408882623`*^9, 
  3.9069639798497252`*^9}},
 CellLabel->"In[77]:=",ExpressionUUID->"506d76d3-db38-48a1-ab47-0179b661d142"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", GridBox[{
     {
      RowBox[{"-", "19.88261904761905`"}], 
      RowBox[{"-", "4.882619047619049`"}], "1.6173809523809528`", 
      "5.2840476190476195`", "7.5340476190476195`", "8.93404761904762`", 
      "9.895714285714286`"},
     {
      RowBox[{"-", "19.866119047619044`"}], 
      RowBox[{"-", "4.866119047619047`"}], "1.6338809523809523`", 
      "5.300547619047618`", "7.550547619047618`", "8.950547619047619`", 
      "9.796714285714286`"},
     {
      RowBox[{"-", "19.864469047619053`"}], 
      RowBox[{"-", "4.864469047619048`"}], "1.6355309523809527`", 
      "5.30219761904762`", "7.55219761904762`", "8.952197619047618`", 
      "9.786814285714286`"}
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
  3.9069638567100844`*^9, {3.906963961510728*^9, 3.90696398205169*^9}, 
   3.9069642541585226`*^9, {3.906965088397904*^9, 3.90696510036639*^9}, 
   3.9720069368539352`*^9},
 CellLabel->
  "Out[78]//MatrixForm=",ExpressionUUID->"369283a8-7527-464f-9975-\
e8ce17b530f2"]
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
  3.906964002951104*^9},ExpressionUUID->"3b55b8d5-405c-44fb-a50f-\
30499d06753d"],

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
 CellLabel->"In[79]:=",ExpressionUUID->"5e673827-b4d3-4e86-b901-8b8527662bcb"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {"0.11881357947081031`"},
      {"0.011881357947080043`"},
      {"0.0011881357947081824`"}
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
   3.904821900050268*^9, 3.906964105372972*^9, 3.906964144147008*^9, 
   3.9069642541785216`*^9, {3.906965072094204*^9, 3.906965100388565*^9}, 
   3.9720069368761864`*^9},
 CellLabel->
  "Out[80]//MatrixForm=",ExpressionUUID->"c86079b5-b7f1-9b4b-9c43-\
7603540e85ba"]
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
        RowBox[{"(", 
         RowBox[{"condA", "*", 
          FractionBox[
           RowBox[{"Norm", "[", 
            RowBox[{"\[CapitalDelta]B", "[", "p", "]"}], "]"}], 
           RowBox[{"Norm", "[", 
            RowBox[{"B", "+", 
             RowBox[{"\[CapitalDelta]B", "[", "p", "]"}]}], "]"}]]}], ")"}], "//",
         " ", "PercentForm"}], ",", 
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
   3.9048218547341175`*^9, 3.904821892883602*^9}, {3.9069649191770477`*^9, 
   3.9069650128177953`*^9}, {3.9069650935118923`*^9, 3.906965096321974*^9}},
 CellLabel->"In[81]:=",ExpressionUUID->"79c29857-762a-42ff-ab92-a20050f72836"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"13%\"\>",
          ShowStringCharacters->False],
         0.1299869652107719,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"1.303%\"\>",
          ShowStringCharacters->False],
         0.013030614935856076`,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"0.1303%\"\>",
          ShowStringCharacters->False],
         0.0013033803942528743`,
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
 CellChangeTimes->{3.906965100404227*^9, 3.972006936897518*^9},
 CellLabel->
  "Out[82]//MatrixForm=",ExpressionUUID->"49a12a54-88c7-f645-8f59-\
2a7490f21e5d"]
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
 CellChangeTimes->{{3.9069640853574314`*^9, 
  3.906964087469249*^9}},ExpressionUUID->"221907ab-bc0d-4e05-9d61-\
b1e42e4cf644"],

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
           RowBox[{"[", "p", "]"}], "]"}], "]"}]], " ", "//", " ", 
        "PercentForm"}], ",", 
       RowBox[{"{", 
        RowBox[{"p", ",", "1", ",", "3", ",", "1"}], "}"}]}], "]"}]}], ";"}], 
   "\[IndentingNewLine]", 
   RowBox[{"\[CurlyEpsilon]", "//", "MatrixForm"}]}]}]], "Input",
 CellChangeTimes->{{3.9048213124423733`*^9, 3.9048213202537007`*^9}, {
  3.904821546757318*^9, 3.9048215497083225`*^9}, {3.9048216167388573`*^9, 
  3.9048216320534625`*^9}, {3.9048216665542483`*^9, 3.9048217347451043`*^9}, {
  3.9069648976386003`*^9, 3.906964908942874*^9}},
 CellLabel->"In[83]:=",ExpressionUUID->"1a46a1eb-8c83-4a97-85db-749af0f49d61"],

Cell[BoxData[
 TagBox[
  RowBox[{"(", "\[NoBreak]", 
   TagBox[GridBox[{
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"0.4542%\"\>",
          ShowStringCharacters->False],
         0.004542287287349712,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"0.04549%\"\>",
          ShowStringCharacters->False],
         0.0004548920623140477,
         AutoDelete->True],
        PercentForm]},
      {
       TagBox[
        InterpretationBox[
         StyleBox["\<\"0.00455%\"\>",
          ShowStringCharacters->False],
         0.000045495813609470354`,
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
 CellChangeTimes->{
  3.9048217368910217`*^9, 3.9048220144259768`*^9, 3.9069642542055235`*^9, 
   3.9069649104637628`*^9, {3.9069650884327545`*^9, 3.906965100432682*^9}, 
   3.9720069369036713`*^9},
 CellLabel->
  "Out[84]//MatrixForm=",ExpressionUUID->"6d7d861c-1c24-3041-8c57-\
a75ee2758611"]
}, Open  ]]
}, Open  ]]
}, Open  ]]
},
WindowSize->{Full, Full},
WindowMargins->{{Automatic, -5}, {-6, Automatic}},
PrintingCopies->1,
PrintingPageRange->{1, Automatic},
PrintingOptions->{"Magnification"->1.,
"PaperOrientation"->"Portrait",
"PaperSize"->{595.2755905511812, 841.8897637795276}},
Magnification:>1. Inherited,
FrontEndVersion->"14.3 for Microsoft Windows (64-bit) (July 8, 2025)",
StyleDefinitions->"Default.nb",
ExpressionUUID->"b8185155-ae23-4c67-bb27-39734f15e6db"
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
Cell[1506, 35, 248, 4, 96, "Title",ExpressionUUID->"046d3c4c-88d4-47a7-835d-2e3a362b76a6"],
Cell[1757, 41, 432, 6, 52, "Subtitle",ExpressionUUID->"78f3ad62-952d-4eb4-809c-3b3153d84216"],
Cell[CellGroupData[{
Cell[2214, 51, 1826, 42, 85, "Input",ExpressionUUID->"436f2075-44db-4973-97ba-a0b70f22ee5f"],
Cell[4043, 95, 1083, 27, 143, "Output",ExpressionUUID->"7d75c1a8-5870-f147-8ab2-d36f4b56717d"]
}, Open  ]],
Cell[CellGroupData[{
Cell[5163, 127, 1074, 28, 85, "Input",ExpressionUUID->"52f22b8e-8c78-4441-bb23-de208cea72de"],
Cell[6240, 157, 906, 29, 143, "Output",ExpressionUUID->"563ce523-a946-8c42-af20-17046cd99749"]
}, Open  ]],
Cell[CellGroupData[{
Cell[7183, 191, 1114, 26, 66, "Input",ExpressionUUID->"6a70395b-8962-483c-bbef-8afe1b33d867"],
Cell[8300, 219, 904, 28, 143, "Output",ExpressionUUID->"6509c465-3054-714a-b122-950197a14001"]
}, Open  ]],
Cell[CellGroupData[{
Cell[9241, 252, 452, 7, 53, "Subsection",ExpressionUUID->"6f0e3deb-e73d-46f1-bc84-ffc659383b26"],
Cell[CellGroupData[{
Cell[9718, 263, 805, 16, 28, "Input",ExpressionUUID->"502a9aee-e08b-47df-94a8-64c5877856b2"],
Cell[10526, 281, 378, 5, 32, "Output",ExpressionUUID->"61b7dfbc-368a-104d-82ea-dd9c6efe0386"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[10953, 292, 437, 7, 53, "Subsection",ExpressionUUID->"a1b0e069-378c-42cd-833d-4b70eea3c783"],
Cell[CellGroupData[{
Cell[11415, 303, 877, 18, 47, "Input",ExpressionUUID->"b2e48c05-1c73-436f-9560-ed778b36ad97"],
Cell[12295, 323, 1381, 38, 50, "Output",ExpressionUUID->"d4be4226-d95a-9347-a100-129c12a7fb02"]
}, Open  ]],
Cell[CellGroupData[{
Cell[13713, 366, 677, 16, 66, "Input",ExpressionUUID->"4e91ca84-e563-4bd3-adc8-226c619e518e"],
Cell[14393, 384, 1100, 36, 199, "Output",ExpressionUUID->"ff715ca6-490b-0548-87e6-b2cae049b40d"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[15542, 426, 848, 14, 105, "Subsection",ExpressionUUID->"70ae7b08-6a93-4e42-be19-258b30f3a8cd"],
Cell[CellGroupData[{
Cell[16415, 444, 2249, 54, 126, "Input",ExpressionUUID->"506d76d3-db38-48a1-ab47-0179b661d142"],
Cell[18667, 500, 1398, 35, 76, "Output",ExpressionUUID->"369283a8-7527-464f-9975-e8ce17b530f2"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[20114, 541, 662, 11, 79, "Subsection",ExpressionUUID->"3b55b8d5-405c-44fb-a50f-30499d06753d"],
Cell[CellGroupData[{
Cell[20801, 556, 1095, 26, 66, "Input",ExpressionUUID->"5e673827-b4d3-4e86-b901-8b8527662bcb"],
Cell[21899, 584, 933, 25, 76, "Output",ExpressionUUID->"c86079b5-b7f1-9b4b-9c43-7603540e85ba"]
}, Open  ]],
Cell[CellGroupData[{
Cell[22869, 614, 1846, 41, 87, "Input",ExpressionUUID->"79c29857-762a-42ff-ab92-a20050f72836"],
Cell[24718, 657, 1279, 43, 76, "Output",ExpressionUUID->"49a12a54-88c7-f645-8f59-2a7490f21e5d"]
}, Open  ]]
}, Open  ]],
Cell[CellGroupData[{
Cell[26046, 706, 1150, 19, 105, "Subsection",ExpressionUUID->"221907ab-bc0d-4e05-9d61-b1e42e4cf644"],
Cell[CellGroupData[{
Cell[27221, 729, 1254, 30, 87, "Input",ExpressionUUID->"1a46a1eb-8c83-4a97-85db-749af0f49d61"],
Cell[28478, 761, 1425, 46, 95, "Output",ExpressionUUID->"6d7d861c-1c24-3041-8c57-a75ee2758611"]
}, Open  ]]
}, Open  ]]
}, Open  ]]
}
]
*)

(* NotebookSignature buTD7WnWctWKVCwTQbidYac4 *)
