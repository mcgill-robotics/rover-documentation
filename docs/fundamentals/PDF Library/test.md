---
 title: "Embedded PDF Example"
 ---

 Below is an embedded PDF file that is hosted locally in the GitHub repository.

 <iframe src="@site/static/pdfs/Jetson_Orin_Nano_Developer_Kit_Carrier_Board_Specification.pdf" width="100%" height="600px">
   This browser does not support PDFs. Please download the PDF to view it: 
   <a href="@site/static/pdfs/Jetson_Orin_Nano_Developer_Kit_Carrier_Board_Specification.pdf">Download PDF</a>.
 </iframe>

 <!-- [View PDF](rover-documentation/static/pdfs/Jetson_Orin_Nano_Developer_Kit_Carrier_Board_Specification.pdf) -->

 <object data="https://www.st.com/resource/en/datasheet/vnh5019a-e.pdf" type="application/pdf" width="700px" height="700px">
     <p>This browser does not support PDFs. Please download the PDF to view it: 
     <a href="https://www.st.com/resource/en/datasheet/vnh5019a-e.pdf">Download PDF</a>.</p>
 </object>

 <iframe src="@site/static/pdfs/Jetson_Orin_Nano_Developer_Kit_Carrier_Board_Specification.pdf" width="100%" height="600px"></iframe>




 ## Hosting the PDF in Docusaurus

 To ensure the PDF is accessible, place it inside the `static` folder of your Docusaurus project:

 ```
 my-docusaurus-project/
 ├── static/
 │   ├── pdfs/
 │   │   ├── example.pdf
 ```

 Docusaurus automatically serves files from `static` at the root URL, so `/pdfs/example.pdf` will be accessible in your site.


 <div style={{ position: 'relative', width: '100%', paddingBottom: '56.25%' }}>

 <iframe src="https://developer.download.nvidia.com/assets/embedded/secure/jetson/orin_nano/docs/Jetson-Orin-Nano-DevKit-Carrier-Board-Specification_SP-11324-001_v1.3.pdf?__token__=exp=1742583283~hmac=ea4dafe85b264b487c62513dcc03030ba8fcb03358ef0691d866bd310675f8be&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9" width="100%" height="600px">
   This browser does not support PDFs. Please download the PDF to view it: 
   <a href="https://developer.download.nvidia.com/assets/embedded/secure/jetson/orin_nano/docs/Jetson-Orin-Nano-DevKit-Carrier-Board-Specification_SP-11324-001_v1.3.pdf?__token__=exp=1742583283~hmac=ea4dafe85b264b487c62513dcc03030ba8fcb03358ef0691d866bd310675f8be&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9">Download PDF</a>.
 </iframe>

 </div>