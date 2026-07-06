import Navbar from "./components/Navbar";

import UploadSection from "./components/UploadSection";

import ActiveDocument from "./components/ActiveDocument";

import ChatWindow from "./components/chat/ChatWindow";

import Sidebar from "./components/Sidebar";

import { ChatProvider } from "./context/ChatContext";

function App() {

  return (

    <ChatProvider>

      <div className="flex h-screen bg-gray-100">

        {/* Sidebar */}

        <Sidebar />

        {/* Main Content */}

        <div className="flex-1 flex flex-col overflow-hidden">

          <Navbar />

          <div className="flex-1 overflow-y-auto">

            <div className="max-w-7xl mx-auto p-6">

              <UploadSection />

              <ActiveDocument />

              <ChatWindow />

            </div>

          </div>

        </div>

      </div>

    </ChatProvider>

  );

}

export default App;