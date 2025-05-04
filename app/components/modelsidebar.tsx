import "@copilotkit/react-ui/styles.css";
import { CopilotKit } from "@copilotkit/react-core"; 
import { CopilotSidebar } from "@copilotkit/react-ui";


export default function modelsidebar({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    return (
        <CopilotKit publicApiKey="<your-copilot-cloud-public-api-key>"> 
        <CopilotSidebar
      defaultOpen={true}
      instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
      labels={{
        title: "Mind Therapy Assistant",
        initial: "How can I help you today?",
      }}
    >
    </CopilotSidebar>
</CopilotKit>
    );
  }
  
 