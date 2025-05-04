import Image from "next/image";
import "@copilotkit/react-ui/styles.css";
import { CopilotKit } from "@copilotkit/react-core"; 
import { CopilotSidebar } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <div className="flex flex-col gap-[16px]">
          <h1 className="text-4xl font-bold">MindMesh</h1>
          <h2 className="text-2xl font-semibold text-gray-500" style={{ fontFamily: "var(--font-geist-sans)" }} >          
            Your AI-Powered Mind Therapy Assistant
          </h2>
          <p className="text-lg text-gray-500">
            MindMesh is a mental health assistant that uses AI to provide personalized support and resources for your mental well-being.
            Whether you're looking for coping strategies, mindfulness exercises, or just someone to talk to, MindMesh is here to help.
            <br />
            <br />
            
          </p>  
          <img src={"/brain.png"} alt="MindMesh" className="w-[1000px] h-[800px]" />
          <p className="text-lg text-gray-500">
            <span className="font-bold">How to use:</span>
            <br />
            1. Ask MindMesh any question related to mental health or well-being.
            <br />
            2. MindMesh will provide personalized responses and resources.
            <br />
            3. Use the resources and strategies provided to support your mental well-being.
            <br />
            4. If you need immediate support, please contact a mental health professional or a crisis hotline.
            <br />
            5. Remember, MindMesh is here to support you, but it is not a substitute for professional mental health care.
            <br />
            6. If you are in crisis or need immediate support, please contact a mental health professional or a crisis hotline.
            <br />
            7. Take care of yourself and reach out for help if you need it.
            <br />
            </p>
            
          </div>
        <div>
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
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
      <span className="font-bold">Disclaimer:</span> MindMesh is not a substitute for professional mental health care. If you are in crisis or need immediate support, please contact a mental health professional or a crisis hotline.
      </footer>
    </div>
  );
}
