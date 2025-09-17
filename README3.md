Building Agents with Lindy Part Two



💡IMPORTANT Make sure you have finished Part One of this project before proceeding
💡IMPORTANT Don’t forget to save your work at every step so that you won’t lose your progress
Visit Lindy AI and sign in. You will then see a page similar to the one below. Click on Create New Lindy to start creating your agent and then on the next window click on Automation





Lindy will then open a Flow Editor similar to the below screen, click on Select Trigger and search for Google Sheets and then New Row Added option. We are choosing this because we want the agent to run as soon as a new record is saved to our Google Sheet.







This action will open a side bar window. This is were you customize all your actions and triggers. As you can see below it is asking us to connect our Google account to Lindy. Click on Connect and give the necessary permission.



Then copy paste the Google Sheet link you obtained earlier to the Spreadsheet ID or URL).



Next click on Search Knowledge Base and provide the google docs link to your CV.

💡 Using Google Docs is not required, you can just copy paste it directly by using the “Text” option
If using Google Docs through Google drive, make sure you give Lindy the required permissions.


On the next window click on Add Google File and select your CV. It will then show you the selected file. Click save and close the dialog window.



Next click the “+” icon followed by Perform an action option, click on Google Docs and then Create Document.







On the left you should see several input fields -

Folder - You can select a folder in your drive where the auto-generated cover letter will be stored. Create a folder if it doesn’t exist, I have named mine job applications.

Title - This field will be used to create the title of the cover letter to be generated. Since we are automating tasks with AI, we will choose to prompt AI to generate a title that matches our application. Select the Prompt AI option.

Prompt for Title- “Write a title in the format of "Cover letter for < company name > : < position >”
Content - We will also choose the Prompt AI option in the content field. In our prompt we will use the requirements filled into our form to generate the relevant cover letter contents.

Prompt for Content- “Write a customized cover letter based on the position, the company, the description of the position, and the requirements [row] .”
Note : Be keen to replace [row] with the rowValues field from the spreadsheet as indicated on the screenshot. Also note that on your side you might not have rowValues depending on the version of google forms you used. If the field available is row, use that instead.


Next add another action by clicking Perform an action option and select Create Document again. We will use this to create the customized CV. Select the same folder (or any folder you want your customized CV to be saved) and use the following prompts:

Prompt for Title “Write a title in the format of "CV for : ”
Prompt for Content “Update my CV from your knowledge base [results] based on the requirements mentioned in [row]”


When writing the content prompt for [results] and [row] click on the spreadsheet and Search results you previously provided by clicking each of the nodes as shown above.
