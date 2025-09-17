# Building Agents with Lindy Part Two

![](https://lh3.googleusercontent.com/d/10Pc-RqDba27kBNm5eym80UDag4YpCKAT)

💡IMPORTANT  Make sure you have finished Part One of this project before proceeding

💡IMPORTANT  Don’t forget to save your work at every step so that you won’t lose your progress

Visit  **[Lindy AI](https://savanna.alxafrica.com/rltoken/EHTlPa7IxRKQCHiHroVGPQ "Lindy AI")** and sign in. You will then see a page similar to the one below. Click on  **Create New Lindy**  to start creating your agent and then on the next window click on  **Automation**

![](https://lh3.googleusercontent.com/d/1k7_fCQAKZg2qL8YrYov9Qb2W13olDd_j)

![](https://lh3.googleusercontent.com/d/1eUR0to50zHXIOjv2M3YY8vR9kB0QiEQ9)

Lindy will then open a  **Flow Editor**  similar to the below screen, click on  **Select Trigger**  and search for  **Google Sheets**  and then  **New Row Added**  option. We are choosing this because we want the agent to run as soon as a new record is saved to our Google Sheet.

![](https://lh3.googleusercontent.com/d/1pDricIUJT-RRKg9dkjfESXg5Kt96Ayxi)

![](https://lh3.googleusercontent.com/d/1gPBbutIbqU_W6KzQ-FZJXN-OrcNUiOaX)

![](https://lh3.googleusercontent.com/d/1Zjqeo0G6gBCExdbdx_zV8RAgAeh-j7Gw)

This action will open a side bar window. This is were you customize all your actions and triggers. As you can see below it is asking us to connect our Google account to Lindy. Click on  **Connect**  and give the necessary permission.

![](https://lh3.googleusercontent.com/d/1bA6NXmkUNiVVX_kb8b8_IGGtGFwNmWz9)

Then copy paste the Google Sheet link you obtained earlier to the  **Spreadsheet ID or URL)**.

![](https://lh3.googleusercontent.com/d/1iZY1cjjP_mxIiyxfm760SuuxJ9Fhe_xU)

Next click on  **Search Knowledge Base**  and provide the google docs link to your CV.

💡 Using Google Docs is not required, you can just copy paste it directly by using the “Text” option  
If using Google Docs through Google drive, make sure you give Lindy the required permissions.

![](https://lh3.googleusercontent.com/d/1Yzfgo7u_SWU3XoQqTkg2w_UQmiyWC7hO)

On the next window click on  **Add Google File**  and select your CV. It will then show you the selected file. Click save and close the dialog window.

![](https://lh3.googleusercontent.com/d/1glDN2lEOHmvgySgfq7ofxPyqXCpqMc1i)

Next click the “+” icon followed by  **Perform an action**  option, click on  **Google Docs**  and then  **Create Document**.

![](https://lh3.googleusercontent.com/d/1e5AL9TYGWmJly1RuyUddPb_XJ1qy3hIy)

![](https://lh3.googleusercontent.com/d/1LF6pI2LaAolGhxgtUAWyKqH0DoSk1YKu)

![](https://lh3.googleusercontent.com/d/1mMo-LfEikP6Ms3AsDC9D3xNhBrDBXPAJ)

On the left you should see several input fields -

**Folder**  - You can select a folder in your drive where the auto-generated cover letter will be stored. Create a folder if it doesn’t exist, I have named mine  `job applications`.

**Title**  - This field will be used to create the title of the cover letter to be generated. Since we are automating tasks with AI, we will choose to prompt AI to generate a title that matches our application. Select the Prompt AI option.

Prompt for Title- “Write a title in the format of "Cover letter for < company name > : < position >”

**Content**  - We will also choose the Prompt AI option in the content field. In our prompt we will use the requirements filled into our form to generate the relevant cover letter contents.

Prompt for Content- “Write a customized cover letter based on the position, the company, the description of the position, and the requirements [row] .”  
Note :  Be keen to replace [row] with the  `rowValues`  field from the spreadsheet as indicated on the screenshot. Also note that on your side you might not have  `rowValues`  depending on the version of google forms you used. If the field available is  `row`, use that instead.

![](https://lh3.googleusercontent.com/d/1pDQ6nj_G_PW8omNknLrSXMFu-NCS3QZU)

Next add another action by clicking  **Perform an action**  option and select  **Create Document**  again. We will use this to create the customized CV. Select the same folder (or any folder you want your customized CV to be saved) and use the following prompts:

Prompt for Title  “Write a title in the format of "CV for  :  ”

Prompt for Content  “Update my CV from your knowledge base [results] based on the requirements mentioned in [row]”

![](https://lh3.googleusercontent.com/d/1HN9u8ei6Qmtfg87rBKokv8yT1Y9a3pg6)

When writing the content prompt for [results] and [row] click on the spreadsheet and Search results you previously provided by clicking each of the nodes as shown above.
