import { useEffect, useRef, useState } from 'react';
import { apiFetch } from '../api';
import { Icon } from './Icons';

const LANGUAGES = [
  { code: 'en', label: 'English', speech: 'en-IN' },
  { code: 'hi', label: 'हिन्दी', speech: 'hi-IN' },
  { code: 'bn', label: 'বাংলা', speech: 'bn-IN' },
];

const SUGGESTIONS = {
  en: [
    'Show low-stock products',
    'What are the pending sales orders?',
    'How do I add a product?',
    'What should I reorder?',
  ],
  hi: [
    'कम स्टॉक वाले उत्पाद दिखाएँ',
    'लंबित बिक्री ऑर्डर कौन से हैं?',
    'उत्पाद कैसे जोड़ें?',
    'मुझे क्या रीऑर्डर करना चाहिए?',
  ],
  bn: [
    'কম স্টকের পণ্য দেখান',
    'কোন বিক্রয় অর্ডারগুলি মুলতুবি আছে?',
    'কীভাবে একটি পণ্য যোগ করব?',
    'আমার কী পুনরায় অর্ডার করা উচিত?',
  ],
};

const UI_TEXT = {
  en: {
    launcher: 'Ask assistant',
    launcherLabel: 'Open NextGenERP Assistant',
    subtitle: 'Project help and live workspace data',
    clear: 'Clear',
    placeholder: 'Ask about stock, orders, suppliers...',
    listening: 'Listening…',
    disclaimer:
      'Only NextGenERP topics. Answers use live workspace data and can be wrong; verify before acting.',
    language: 'Answer language',
    voiceInput: 'Ask by voice',
    stopListening: 'Stop listening',
    voiceUnsupported: 'Voice input is not supported in this browser',
    speak: 'Play answer aloud',
    stopSpeaking: 'Stop playback',
    autoSpeak: 'Auto-speak answers',
    speechUnsupported: 'Spoken replies are not supported in this browser',
    speechVoiceMissing:
      'No {language} voice is installed on this device. Add it in Windows Settings > Time & language > Language & region, then restart the browser. The written answer is still available.',
    thinking: 'Assistant is thinking',
    welcome:
      "Hi! I'm the NextGenERP Assistant. I can answer questions about this workspace using live inventory, order and supplier data. I only cover NextGenERP topics.",
    micDenied:
      'Microphone permission was denied. Allow microphone access and try again.',
    micNoSpeech: 'No speech was detected. Try again.',
    micNoDevice: 'No microphone was found.',
    micNetwork:
      'Voice recognition is unavailable right now. Check your connection or type your question.',
    micError: 'Voice input could not start. Please type your question.',
    micLanguage:
      'Voice recognition does not support the selected language in this browser. Choose another language or type your question.',
    micTimeout:
      'No speech was detected in time. Try again and speak after the microphone starts.',
    micBusy: 'Voice input is already starting. Please wait a moment.',
    micStopped: 'Voice input stopped.',
    secureContext:
      'Voice input needs a secure connection. Open the app over HTTPS or on localhost, or type your question.',
    interim: 'Heard',
    retry: 'Retry',
    assistantError: 'The assistant could not answer right now',
    unreachable:
      'Cannot reach the assistant. Check that the backend is running.',
    fallbackReply: 'I could not generate an answer for that.',
    close: 'Close assistant',
    panelLabel: 'NextGenERP Assistant',
    messageLabel: 'Message the NextGenERP Assistant',
    send: 'Send message',
  },
  hi: {
    launcher: 'सहायक से पूछें',
    launcherLabel: 'NextGenERP सहायक खोलें',
    subtitle: 'प्रोजेक्ट सहायता और लाइव वर्कस्पेस डेटा',
    clear: 'साफ़ करें',
    placeholder: 'स्टॉक, ऑर्डर, आपूर्तिकर्ता के बारे में पूछें...',
    listening: 'सुन रहा हूँ…',
    disclaimer:
      'केवल NextGenERP विषय। उत्तर लाइव वर्कस्पेस डेटा से हैं और गलत हो सकते हैं; कार्रवाई से पहले जाँचें।',
    language: 'उत्तर की भाषा',
    voiceInput: 'बोलकर पूछें',
    stopListening: 'सुनना बंद करें',
    voiceUnsupported: 'इस ब्राउज़र में वॉइस इनपुट समर्थित नहीं है',
    speak: 'उत्तर सुनें',
    stopSpeaking: 'प्लेबैक रोकें',
    autoSpeak: 'उत्तर स्वतः सुनें',
    speechUnsupported: 'इस ब्राउज़र में बोलकर उत्तर सुनाना समर्थित नहीं है',
    speechVoiceMissing:
      'इस डिवाइस पर {language} की आवाज़ इंस्टॉल नहीं है। Windows सेटिंग्स > समय और भाषा > भाषा और क्षेत्र में इसे जोड़ें, फिर ब्राउज़र फिर से चालू करें। लिखित उत्तर अभी भी उपलब्ध है।',
    thinking: 'सहायक सोच रहा है',
    welcome:
      'नमस्ते! मैं NextGenERP सहायक हूँ। मैं लाइव इन्वेंटरी, ऑर्डर और आपूर्तिकर्ता डेटा से इस वर्कस्पेस के बारे में उत्तर दे सकता हूँ। मैं केवल NextGenERP विषयों में मदद करता हूँ।',
    micDenied:
      'माइक्रोफ़ोन अनुमति अस्वीकृत हुई। अनुमति दें और फिर प्रयास करें।',
    micNoSpeech: 'कोई आवाज़ नहीं मिली। फिर प्रयास करें।',
    micNoDevice: 'कोई माइक्रोफ़ोन नहीं मिला।',
    micNetwork:
      'वॉइस पहचान अभी उपलब्ध नहीं है। कनेक्शन जाँचें या प्रश्न टाइप करें।',
    micError: 'वॉइस इनपुट शुरू नहीं हो सका। कृपया प्रश्न टाइप करें।',
    micLanguage:
      'इस ब्राउज़र में चुनी गई भाषा के लिए वॉइस पहचान समर्थित नहीं है। दूसरी भाषा चुनें या प्रश्न टाइप करें।',
    micTimeout:
      'समय पर कोई आवाज़ नहीं मिली। फिर प्रयास करें और माइक्रोफ़ोन शुरू होने के बाद बोलें।',
    micBusy: 'वॉइस इनपुट पहले से शुरू हो रहा है। कृपया प्रतीक्षा करें।',
    micStopped: 'वॉइस इनपुट रुक गया।',
    secureContext:
      'वॉइस इनपुट के लिए सुरक्षित कनेक्शन आवश्यक है। ऐप को HTTPS या localhost पर खोलें, या प्रश्न टाइप करें।',
    interim: 'सुना',
    retry: 'फिर प्रयास करें',
    assistantError: 'सहायक अभी उत्तर नहीं दे सका',
    unreachable: 'सहायक से संपर्क नहीं हो रहा। जाँचें कि बैकएंड चल रहा है।',
    fallbackReply: 'मैं उसका उत्तर नहीं बना सका।',
    close: 'सहायक बंद करें',
    panelLabel: 'NextGenERP सहायक',
    messageLabel: 'NextGenERP सहायक को संदेश भेजें',
    send: 'संदेश भेजें',
  },
  bn: {
    launcher: 'সহায়ককে জিজ্ঞাসা করুন',
    launcherLabel: 'NextGenERP সহায়ক খুলুন',
    subtitle: 'প্রকল্প সহায়তা এবং লাইভ ওয়ার্কস্পেস ডেটা',
    clear: 'মুছুন',
    placeholder: 'স্টক, অর্ডার, সরবরাহকারী সম্পর্কে জিজ্ঞাসা করুন...',
    listening: 'শুনছি…',
    disclaimer:
      'শুধু NextGenERP বিষয়। উত্তর লাইভ ওয়ার্কস্পেস ডেটা থেকে আসে এবং ভুল হতে পারে; ব্যবস্থা নেওয়ার আগে যাচাই করুন।',
    language: 'উত্তরের ভাষা',
    voiceInput: 'কণ্ঠে জিজ্ঞাসা করুন',
    stopListening: 'শোনা বন্ধ করুন',
    voiceUnsupported: 'এই ব্রাউজারে কণ্ঠ ইনপুট সমর্থিত নয়',
    speak: 'উত্তর শুনুন',
    stopSpeaking: 'প্লেব্যাক বন্ধ করুন',
    autoSpeak: 'উত্তর স্বয়ংক্রিয়ভাবে শুনুন',
    speechUnsupported: 'এই ব্রাউজারে কথা বলে উত্তর শোনানো সমর্থিত নয়',
    speechVoiceMissing:
      'এই ডিভাইসে {language} কণ্ঠস্বর ইনস্টল নেই। Windows সেটিংস > সময় ও ভাষা > ভাষা ও অঞ্চলে এটি যোগ করুন, তারপর ব্রাউজার আবার চালু করুন। লিখিত উত্তর এখনও পাওয়া যাচ্ছে।',
    thinking: 'সহায়ক ভাবছে',
    welcome:
      'নমস্কার! আমি NextGenERP সহায়ক। আমি লাইভ ইনভেন্টরি, অর্ডার ও সরবরাহকারী ডেটা ব্যবহার করে এই ওয়ার্কস্পেস সম্পর্কে উত্তর দিতে পারি। আমি শুধু NextGenERP বিষয়ে সাহায্য করি।',
    micDenied:
      'মাইক্রোফোন অনুমতি প্রত্যাখ্যাত হয়েছে। অনুমতি দিয়ে আবার চেষ্টা করুন।',
    micNoSpeech: 'কোনো কথা শোনা যায়নি। আবার চেষ্টা করুন।',
    micNoDevice: 'কোনো মাইক্রোফোন পাওয়া যায়নি।',
    micNetwork:
      'কণ্ঠ শনাক্তকরণ এখন উপলব্ধ নয়। সংযোগ পরীক্ষা করুন বা প্রশ্ন টাইপ করুন।',
    micError: 'কণ্ঠ ইনপুট শুরু করা যায়নি। অনুগ্রহ করে প্রশ্ন টাইপ করুন।',
    micLanguage:
      'এই ব্রাউজারে নির্বাচিত ভাষার জন্য কণ্ঠ শনাক্তকরণ সমর্থিত নয়। অন্য ভাষা বেছে নিন বা প্রশ্ন টাইপ করুন।',
    micTimeout:
      'সময়ে কোনো কথা শোনা যায়নি। আবার চেষ্টা করুন এবং মাইক্রোফোন চালু হওয়ার পরে বলুন।',
    micBusy: 'কণ্ঠ ইনপুট ইতিমধ্যে শুরু হচ্ছে। অনুগ্রহ করে অপেক্ষা করুন।',
    micStopped: 'কণ্ঠ ইনপুট বন্ধ হয়েছে।',
    secureContext:
      'কণ্ঠ ইনপুটের জন্য নিরাপদ সংযোগ প্রয়োজন। HTTPS বা localhost ব্যবহার করুন, অথবা প্রশ্ন টাইপ করুন।',
    interim: 'শোনা গেছে',
    retry: 'আবার চেষ্টা করুন',
    assistantError: 'সহায়ক এখন উত্তর দিতে পারেনি',
    unreachable: 'সহায়কের সাথে সংযোগ হচ্ছে না। ব্যাকএন্ড চলছে কিনা দেখুন।',
    fallbackReply: 'আমি এর উত্তর তৈরি করতে পারিনি।',
    close: 'সহায়ক বন্ধ করুন',
    panelLabel: 'NextGenERP সহায়ক',
    messageLabel: 'NextGenERP সহায়ককে বার্তা পাঠান',
    send: 'বার্তা পাঠান',
  },
};

function welcomeMessage(language) {
  return {
    role: 'assistant',
    content: UI_TEXT[language].welcome,
  };
}

function getSpeechRecognition() {
  if (typeof window === 'undefined') return null;
  return window.SpeechRecognition || window.webkitSpeechRecognition || null;
}

function canSpeak() {
  return (
    typeof window !== 'undefined' &&
    'speechSynthesis' in window &&
    typeof window.SpeechSynthesisUtterance === 'function'
  );
}

function speechLocale(language) {
  return LANGUAGES.find((item) => item.code === language)?.speech || 'en-IN';
}

function voiceMissingMessage(language) {
  const label = LANGUAGES.find((item) => item.code === language)?.label || language;
  return UI_TEXT[language].speechVoiceMissing.replace('{language}', label);
}

const RECOGNITION_TIMEOUT_MS = 15000;

function hasSecureContext() {
  if (typeof window === 'undefined') return false;
  if (window.isSecureContext) return true;
  const hostname = window.location?.hostname ?? '';
  return hostname === 'localhost' || hostname === '127.0.0.1' || hostname === '[::1]';
}

function pickVoice(voices, locale, language) {
  if (!Array.isArray(voices) || voices.length === 0) return null;
  const wantedLocale = locale.toLowerCase();
  const wantedLanguage = language.toLowerCase();
  const byLocale = voices.find(
    (voice) => (voice.lang || '').toLowerCase() === wantedLocale,
  );
  if (byLocale) return byLocale;
  const byLanguage = voices.find(
    (voice) => (voice.lang || '').toLowerCase().split('-')[0] === wantedLanguage,
  );
  if (byLanguage) return byLanguage;
  return (
    voices.find((voice) =>
      (voice.lang || '').toLowerCase().startsWith(wantedLanguage),
    ) || null
  );
}

function getErrorMessage(data, fallback) {
  if (typeof data.detail === 'string') return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail.map((issue) => issue.msg).filter(Boolean).join(' ');
  }
  return fallback;
}

export default function Assistant() {
  const [open, setOpen] = useState(false);
  const [language, setLanguage] = useState('en');
  const [messages, setMessages] = useState(() => [welcomeMessage('en')]);
  const [suggestions, setSuggestions] = useState(SUGGESTIONS.en);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const [voiceError, setVoiceError] = useState('');
  const [lastAttempt, setLastAttempt] = useState(null);
  const [listening, setListening] = useState(false);
  const [starting, setStarting] = useState(false);
  const [interimText, setInterimText] = useState('');
  const [voices, setVoices] = useState([]);
  const [speakingText, setSpeakingText] = useState('');
  const [autoSpeak, setAutoSpeak] = useState(false);
  const logRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);
  const recognitionTimeoutRef = useRef(null);
  const recognitionTimedOutRef = useRef(false);
  const startingRef = useRef(false);
  const submitRef = useRef(null);
  const requestSeqRef = useRef(0);

  const copy = UI_TEXT[language];
  const recognitionSupported = Boolean(getSpeechRecognition());
  const secureContext = hasSecureContext();
  const voiceInputAvailable = recognitionSupported && secureContext;
  const speechSupported = canSpeak();

  useEffect(() => {
    if (open) inputRef.current?.focus();
  }, [open]);

  useEffect(() => {
    if (!canSpeak()) return undefined;
    const synth = window.speechSynthesis;
    function loadVoices() {
      try {
        setVoices(synth.getVoices() || []);
      } catch {
        setVoices([]);
      }
    }
    loadVoices();
    if (typeof synth.addEventListener === 'function') {
      synth.addEventListener('voiceschanged', loadVoices);
      return () => synth.removeEventListener('voiceschanged', loadVoices);
    }
    synth.onvoiceschanged = loadVoices;
    return () => {
      synth.onvoiceschanged = null;
    };
  }, []);

  useEffect(() => {
    if (!open) return;
    const log = logRef.current;
    if (log) log.scrollTop = log.scrollHeight;
  }, [messages, sending, open]);

  useEffect(() => {
    if (!open) return undefined;

    function handleKeyDown(event) {
      if (event.key !== 'Escape') return;
      stopListening();
      stopSpeaking();
      setOpen(false);
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [open]);

  useEffect(() => {
    return () => {
      clearRecognitionTimeout();
      startingRef.current = false;
      const recognition = recognitionRef.current;
      recognitionRef.current = null;
      if (recognition) {
        try {
          recognition.abort();
        } catch {
          // Recognition may already be stopped.
        }
      }
      if (canSpeak()) window.speechSynthesis.cancel();
    };
  }, []);

  function clearRecognitionTimeout() {
    if (recognitionTimeoutRef.current !== null) {
      window.clearTimeout(recognitionTimeoutRef.current);
      recognitionTimeoutRef.current = null;
    }
  }

  function stopSpeaking() {
    if (canSpeak()) window.speechSynthesis.cancel();
    setSpeakingText('');
  }

  function speak(replyText) {
    if (!speechSupported) {
      setVoiceError(copy.speechUnsupported);
      return;
    }
    if (speakingText === replyText) {
      stopSpeaking();
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new window.SpeechSynthesisUtterance(replyText);
    const locale = speechLocale(language);
    utterance.lang = locale;
    utterance.rate = 0.98;

    let availableVoices = [];
    try {
      availableVoices = voices.length
        ? voices
        : window.speechSynthesis.getVoices() || [];
      const voice = pickVoice(availableVoices, locale, language);
      if (!voice && availableVoices.length > 0 && language !== 'en') {
        // Speaking Bengali/Hindi text with an English voice is unintelligible.
        // Explain the missing voice instead of playing the wrong language.
        setVoiceError(voiceMissingMessage(language));
        return;
      }
      if (voice) utterance.voice = voice;
    } catch {
      // Voice selection is best-effort; the default voice still works.
    }

    const clearIfCurrent = () =>
      setSpeakingText((current) => (current === replyText ? '' : current));

    utterance.onend = clearIfCurrent;
    utterance.onerror = (event) => {
      clearIfCurrent();
      const code = event?.error;
      if (['language-unavailable', 'voice-unavailable'].includes(code)) {
        setVoiceError(voiceMissingMessage(language));
      } else if (!['interrupted', 'canceled', 'cancelled'].includes(code)) {
        setVoiceError(copy.speechUnsupported);
      }
    };
    setSpeakingText(replyText);
    window.speechSynthesis.speak(utterance);
  }

  function stopListening() {
    clearRecognitionTimeout();
    recognitionTimedOutRef.current = false;
    startingRef.current = false;
    const recognition = recognitionRef.current;
    recognitionRef.current = null;
    setListening(false);
    setStarting(false);
    setInterimText('');
    if (recognition) {
      try {
        recognition.abort();
      } catch {
        try {
          recognition.stop();
        } catch {
          // Recognition may already be stopped.
        }
      }
    }
  }

  function startListening() {
    const SpeechRecognition = getSpeechRecognition();
    if (!secureContext) {
      setVoiceError(copy.secureContext);
      return;
    }
    if (!SpeechRecognition) {
      setVoiceError(copy.voiceUnsupported);
      return;
    }
    if (listening) {
      stopListening();
      return;
    }
    if (starting || startingRef.current) {
      setVoiceError(copy.micBusy);
      return;
    }
    if (sending) return;

    stopSpeaking();
    setVoiceError('');
    setError('');
    setInterimText('');
    recognitionTimedOutRef.current = false;

    const recognition = new SpeechRecognition();
    recognition.lang = speechLocale(language);
    recognition.interimResults = true;
    recognition.continuous = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      if (recognitionRef.current !== recognition) return;
      startingRef.current = false;
      setStarting(false);
      setListening(true);
      clearRecognitionTimeout();
      recognitionTimeoutRef.current = window.setTimeout(() => {
        if (recognitionRef.current !== recognition) return;
        recognitionTimedOutRef.current = true;
        setVoiceError(copy.micTimeout);
        setInterimText('');
        try {
          recognition.stop();
        } catch {
          try {
            recognition.abort();
          } catch {
            // Recognition may already be stopped.
          }
        }
      }, RECOGNITION_TIMEOUT_MS);
    };

    recognition.onresult = (event) => {
      if (recognitionRef.current !== recognition) return;
      let interim = '';
      let final = '';
      for (
        let index = event.resultIndex ?? 0;
        index < event.results.length;
        index += 1
      ) {
        const result = event.results[index];
        const transcript = result?.[0]?.transcript ?? '';
        if (result.isFinal) final += transcript;
        else interim += transcript;
      }
      if (interim.trim()) setInterimText(interim.trim());
      if (final.trim()) {
        clearRecognitionTimeout();
        setInterimText('');
        setInput('');
        submitRef.current?.(final.trim());
      }
    };

    recognition.onerror = (event) => {
      if (recognitionRef.current !== recognition) return;
      clearRecognitionTimeout();
      startingRef.current = false;
      const code = event?.error;
      if (code === 'aborted') {
        setInterimText('');
        return;
      }
      if (code === 'not-allowed' || code === 'service-not-allowed') {
        setVoiceError(copy.micDenied);
      } else if (code === 'no-speech') {
        setVoiceError(
          recognitionTimedOutRef.current ? copy.micTimeout : copy.micNoSpeech,
        );
      } else if (code === 'audio-capture') {
        setVoiceError(copy.micNoDevice);
      } else if (code === 'network') {
        setVoiceError(copy.micNetwork);
      } else if (code === 'language-not-supported') {
        setVoiceError(copy.micLanguage);
      } else if (code === 'busy') {
        setVoiceError(copy.micBusy);
      } else {
        setVoiceError(copy.micError);
      }
    };

    recognition.onend = () => {
      clearRecognitionTimeout();
      startingRef.current = false;
      if (recognitionRef.current === recognition) recognitionRef.current = null;
      setListening(false);
      setStarting(false);
      setInterimText('');
    };

    recognitionRef.current = recognition;
    startingRef.current = true;
    setStarting(true);
    try {
      recognition.start();
    } catch {
      clearRecognitionTimeout();
      startingRef.current = false;
      recognitionRef.current = null;
      setStarting(false);
      setListening(false);
      setVoiceError(copy.micError);
    }
  }

  async function requestReply(content, history) {
    const requestId = ++requestSeqRef.current;
    setSending(true);
    setError('');
    setVoiceError('');
    setLastAttempt({ content, history });

    try {
      const response = await apiFetch('/assistant/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: content, history, language }),
      });
      const data = await response.json().catch(() => ({}));

      if (requestId !== requestSeqRef.current) return;

      if (!response.ok) {
        throw new Error(
          getErrorMessage(
            data,
            `${copy.assistantError} (HTTP ${response.status}).`,
          ),
        );
      }

      const reply = data.reply || copy.fallbackReply;
      setMessages((current) => [
        ...current,
        { role: 'assistant', content: reply },
      ]);
      if (Array.isArray(data.suggestions) && data.suggestions.length) {
        setSuggestions(data.suggestions);
      }
      setLastAttempt(null);
      if (autoSpeak && speechSupported) speak(reply);
    } catch (requestError) {
      if (requestId !== requestSeqRef.current) return;
      setError(
        requestError instanceof TypeError
          ? copy.unreachable
          : requestError.message,
      );
    } finally {
      if (requestId === requestSeqRef.current) setSending(false);
    }
  }

  function submitContent(rawContent) {
    const content = rawContent.trim();
    if (!content || sending) return;

    const history = messages.slice(-8).map(({ role, content: text }) => ({
      role,
      content: text,
    }));

    setMessages((current) => [...current, { role: 'user', content }]);
    setInput('');
    requestReply(content, history);
  }

  submitRef.current = submitContent;

  function handleSubmit(event) {
    event.preventDefault();
    submitContent(input);
  }

  function retry() {
    if (lastAttempt && !sending) {
      requestReply(lastAttempt.content, lastAttempt.history);
    }
  }

  function clearChat() {
    stopListening();
    stopSpeaking();
    requestSeqRef.current += 1;
    setSending(false);
    setMessages([welcomeMessage(language)]);
    setSuggestions(SUGGESTIONS[language]);
    setInput('');
    setError('');
    setVoiceError('');
    setLastAttempt(null);
  }

  function handleLanguageChange(event) {
    const nextLanguage = event.target.value;
    if (!UI_TEXT[nextLanguage]) return;

    stopListening();
    stopSpeaking();
    requestSeqRef.current += 1;
    setSending(false);
    setLanguage(nextLanguage);
    setMessages([welcomeMessage(nextLanguage)]);
    setSuggestions(SUGGESTIONS[nextLanguage]);
    setInput('');
    setError('');
    setVoiceError('');
    setLastAttempt(null);
  }

  function toggleAutoSpeak() {
    if (!speechSupported) {
      setVoiceError(copy.speechUnsupported);
      return;
    }
    const next = !autoSpeak;
    setAutoSpeak(next);
    if (!next) stopSpeaking();
  }

  function handleClose() {
    stopListening();
    stopSpeaking();
    requestSeqRef.current += 1;
    setSending(false);
    setOpen(false);
  }

  const visibleError = error || voiceError;

  if (!open) {
    return (
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-expanded="false"
        aria-controls="assistant-panel"
        className="fixed bottom-4 right-4 z-40 inline-flex items-center gap-2 rounded-full bg-stone-900 py-2.5 pl-2.5 pr-4 text-sm font-semibold text-white shadow-[0_18px_40px_-18px_rgba(28,25,23,0.9)] transition hover:bg-stone-800 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:ring-offset-2"
      >
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-teal-300 to-emerald-400 text-[#06201d]">
          <Icon name="spark" size={16} />
        </span>
        <span className="hidden sm:inline">{copy.launcher}</span>
        <span className="sr-only sm:hidden">{copy.launcherLabel}</span>
      </button>
    );
  }

  return (
    <section
      id="assistant-panel"
      aria-label={copy.panelLabel}
      className="fixed inset-x-3 bottom-3 z-50 flex h-[min(34rem,calc(100vh-1.5rem))] flex-col overflow-hidden rounded-2xl border border-stone-200 bg-[#fffdf9] shadow-[0_30px_80px_-30px_rgba(28,25,23,0.7)] sm:inset-x-auto sm:bottom-5 sm:right-5 sm:w-[24rem]"
    >
      <header className="flex items-center gap-3 border-b border-stone-200 bg-gradient-to-r from-[#12181a] via-[#0f1517] to-[#0b1112] px-4 py-3 text-stone-100">
        <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-400/15 text-teal-200">
          <Icon name="spark" size={17} />
        </span>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold tracking-tight">
            NextGenERP Assistant
          </p>
          <p className="truncate text-[10px] text-stone-400">{copy.subtitle}</p>
        </div>
        <button
          type="button"
          onClick={handleClose}
          aria-label={copy.close}
          className="rounded-md p-1.5 text-stone-400 transition hover:bg-white/10 hover:text-white"
        >
          <Icon name="close" size={16} />
        </button>
      </header>

      <div className="flex flex-wrap items-center gap-2 border-b border-stone-200 bg-stone-50/80 px-3 py-2">
        <label className="inline-flex items-center gap-1.5 text-[11px] font-medium text-stone-600">
          <Icon name="globe" size={13} />
          <span className="sr-only">{copy.language}</span>
          <select
            value={language}
            onChange={handleLanguageChange}
            aria-label={copy.language}
            className="rounded-md border border-stone-300 bg-white px-2 py-1 text-[11px] font-medium text-stone-700 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
          >
            {LANGUAGES.map((item) => (
              <option key={item.code} value={item.code}>
                {item.label}
              </option>
            ))}
          </select>
        </label>

        <button
          type="button"
          onClick={toggleAutoSpeak}
          disabled={!speechSupported}
          aria-pressed={autoSpeak}
          aria-label={copy.autoSpeak}
          title={speechSupported ? copy.autoSpeak : copy.speechUnsupported}
          className={`inline-flex items-center gap-1.5 rounded-md border px-2 py-1 text-[11px] font-medium transition disabled:cursor-not-allowed disabled:opacity-40 ${
            autoSpeak
              ? 'border-teal-300 bg-teal-50 text-teal-800'
              : 'border-stone-300 bg-white text-stone-600 hover:bg-stone-50'
          }`}
        >
          <Icon name={autoSpeak ? 'volume' : 'volumeOff'} size={13} />
          <span className="hidden sm:inline">{copy.autoSpeak}</span>
        </button>

        <button
          type="button"
          onClick={clearChat}
          className="ml-auto rounded-md px-2 py-1 text-[11px] font-medium text-stone-500 transition hover:bg-stone-200/70 hover:text-stone-800"
        >
          {copy.clear}
        </button>
      </div>

      <div
        ref={logRef}
        role="log"
        aria-live="polite"
        aria-relevant="additions"
        className="flex-1 space-y-3 overflow-y-auto px-4 py-4"
      >
        {messages.map((message, index) => {
          const isSpeaking = speakingText === message.content;
          return (
            <div
              key={`${message.role}-${index}`}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
                  message.role === 'user'
                    ? 'rounded-br-md bg-teal-700 text-white'
                    : 'rounded-bl-md border border-stone-200 bg-white text-stone-700'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                {message.role === 'assistant' && (
                  <button
                    type="button"
                    onClick={() => speak(message.content)}
                    disabled={!speechSupported}
                    aria-label={
                      isSpeaking ? copy.stopSpeaking : copy.speak
                    }
                    title={speechSupported ? copy.speak : copy.speechUnsupported}
                    className={`mt-1.5 inline-flex items-center gap-1 rounded-md px-1.5 py-0.5 text-[10px] font-medium transition disabled:cursor-not-allowed disabled:opacity-40 ${
                      isSpeaking
                        ? 'bg-teal-50 text-teal-700'
                        : 'text-stone-400 hover:bg-stone-100 hover:text-stone-700'
                    }`}
                  >
                    <Icon
                      name={isSpeaking ? 'volumeOff' : 'volume'}
                      size={12}
                    />
                    <span className="sr-only">
                      {isSpeaking ? copy.stopSpeaking : copy.speak}
                    </span>
                  </button>
                )}
              </div>
            </div>
          );
        })}

        {sending && (
          <div className="flex justify-start">
            <div className="flex items-center gap-1.5 rounded-2xl rounded-bl-md border border-stone-200 bg-white px-3.5 py-3 text-stone-500">
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400 [animation-delay:-0.2s]" />
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400 [animation-delay:-0.1s]" />
              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400" />
              <span className="sr-only">{copy.thinking}</span>
            </div>
          </div>
        )}

      </div>

      {visibleError && (
        <div
          role="alert"
          className="mx-3 mb-2 flex items-start justify-between gap-2 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-xs text-rose-800"
        >
          <span>{visibleError}</span>
          {error && lastAttempt && (
            <button
              type="button"
              onClick={retry}
              className="shrink-0 font-semibold underline decoration-rose-300 underline-offset-2 hover:decoration-rose-600"
            >
              {copy.retry}
            </button>
          )}
        </div>
      )}

      {!sending && suggestions.length > 0 && (
        <div className="flex flex-wrap gap-1.5 border-t border-stone-100 px-3 pt-2.5">
          {suggestions.slice(0, 4).map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => submitContent(suggestion)}
              className="rounded-full border border-stone-200 bg-stone-50 px-2.5 py-1 text-[11px] font-medium text-stone-600 transition hover:border-teal-300 hover:bg-teal-50 hover:text-teal-800"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit} className="border-t border-stone-200 p-3">
        <div className="flex items-end gap-2">
          <button
            type="button"
            onClick={startListening}
            disabled={!voiceInputAvailable || sending || starting}
            aria-pressed={listening}
            aria-label={
              starting
                ? copy.micBusy
                : listening
                  ? copy.stopListening
                  : copy.voiceInput
            }
            title={
              !secureContext
                ? copy.secureContext
                : recognitionSupported
                  ? starting
                    ? copy.micBusy
                    : listening
                      ? copy.stopListening
                      : copy.voiceInput
                  : copy.voiceUnsupported
            }
            className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg border transition disabled:cursor-not-allowed disabled:opacity-40 ${
              listening
                ? 'border-rose-300 bg-rose-50 text-rose-600'
                : 'border-stone-300 bg-white text-stone-600 hover:bg-stone-50'
            }`}
          >
            <Icon name="mic" size={16} />
          </button>
          <input
            ref={inputRef}
            value={input}
            onChange={(event) => setInput(event.target.value)}
            maxLength={1000}
            placeholder={listening ? copy.listening : copy.placeholder}
            aria-label={copy.messageLabel}
            className="min-w-0 flex-1 rounded-lg border border-stone-300 bg-white px-3 py-2.5 text-sm text-stone-800 outline-none placeholder:text-stone-400 focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
          />
          <button
            type="submit"
            disabled={sending || !input.trim()}
            aria-label={copy.send}
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-stone-900 text-white transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-40"
          >
            <Icon name="send" size={16} />
          </button>
        </div>
        {listening && interimText && (
          <p
            aria-live="polite"
            className="mt-2 rounded-md border border-teal-200 bg-teal-50 px-2 py-1.5 text-xs text-teal-900"
          >
            <span className="font-semibold">{copy.interim}:</span> {interimText}
          </p>
        )}
        {!secureContext && (
          <p className="mt-2 text-[10px] leading-snug text-amber-700">
            {copy.secureContext}
          </p>
        )}
        <p className="mt-2 text-[10px] leading-snug text-stone-400">
          {starting ? (
            <span className="inline-flex items-center gap-1.5 text-stone-500">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-stone-400" />
              {copy.micBusy}
            </span>
          ) : listening ? (
            <span className="inline-flex items-center gap-1.5 text-rose-600">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-rose-500" />
              {copy.listening}
            </span>
          ) : (
            copy.disclaimer
          )}
        </p>
      </form>
    </section>
  );
}
