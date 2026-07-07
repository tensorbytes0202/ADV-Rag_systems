import { useState } from "react";

import Navbar from "./components/Navbar";
import UploadSection from "./components/UploadSection";
import ActiveDocument from "./components/ActiveDocument";
import ChatWindow from "./components/chat/ChatWindow";
import Sidebar from "./components/Sidebar";
import PDFViewer from "./components/PDFViewer";

import { ChatProvider } from "./context/ChatContext";

function App() {

  // ==========================
  // Active PDF
  // ==========================

  const [activeDocument, setActiveDocument] = useState("");

  return (

    <ChatProvider>

      <div className="flex h-screen bg-gray-100">

        {/* Sidebar */}

        <Sidebar />

        {/* Main Area */}

        <div className="flex-1 flex flex-col overflow-hidden">

          <Navbar />

          <div className="flex-1 overflow-y-auto">

            <div className="max-w-7xl mx-auto p-6">

              {/* Upload */}

              <UploadSection />

              {/* Active Document */}

              <ActiveDocument

                activeDocument={activeDocument}

                setActiveDocument={setActiveDocument}

              />

              {/* Chat + PDF */}

              <div className="grid grid-cols-12 gap-6 mt-6">

                {/* Chat */}

                <div className="col-span-7">

                  <ChatWindow />

                </div>

                {/* PDF */}

                <div className="col-span-5">

                  <PDFViewer

                    filename={activeDocument}

                  />

                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </ChatProvider>

  );

}

export default App;