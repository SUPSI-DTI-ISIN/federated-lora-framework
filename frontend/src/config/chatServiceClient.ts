import {Configuration, ChatApi, MessagesApi} from "@isin/chat-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const chatApi = new ChatApi(config);
export const messagesApi = new MessagesApi(config);